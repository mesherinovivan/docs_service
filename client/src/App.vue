<template>
  <div>
    <select v-model="selectedForm">
      <option :key="f" :value="f.filename"  v-for="f in forms">{{f.filename}}</option>
    </select>
    <button  v-if="htmlForm" @click="onDownloadClick">Download</button>
    <component ref="htmlFormComponent" v-if="htmlForm" :is="formComponent"></component>
  </div>
</template>

<script>
  import axios from 'axios';

  export default {
    data() {
      // данные приложения
      return {
        selectedForm: null,
        htmlForm: null,
        forms: []
      }
    },
    created() {
      // при инициализации компонента делаем запрос всех docx форм
      axios("/api/form")
        .then(response => this.forms = response.data.forms) // и сохраняем список в переменную forms
    },
    watch: {
      selectedForm() {
        // остлеживаем изменения выпадающего списка
        // и при его изменении запрашиваем его html содержимое
        axios(`/api/form/${this.selectedForm}`).then(response => {
          let html = response.data.html.replace(
              /\{\{(\w+)\}\}/g,
            '<input ref="$1" placeholder="$1">'
          );
          this.htmlForm = html; // и сохраняем в переменную htmlForm
        })
      }
    },
      computed: {
        // наш динамичский компонент который формируется на основе html
        formComponent() {
          return {
            // пришлось обернуть в div, так как шаблон
            // может иметь только один корневой тэг
            template: `<div>${this.htmlForm}</div>`,
          }
        },
      },
      methods: {
        onDownloadClick () {
          let data = this.$refs.htmlFormComponent.$refs;

          // формируем строку параметров get запроса
          let params = Object.keys(data).map(function (key) {
            return [key, data[key].value].map(encodeURIComponent).join("=");
          }).join("&");

          // формируем url, передавать параметры get запросом не очень хорошая идея,
          // но для тестового приложения пойдет
          let url = `/api/form/print/${this.selectedForm}?${params}`;
          window.open(url);
        }
    }
    
  }
</script>