<template>
  <v-alert :type="type" color="white rounded-0" elevation="3">
    <template v-slot:prepend>
        <v-icon outlined :color="type">{{icon}}</v-icon>
    </template>
    <template v-slot:default>
        <div class="d-flex" :class="typeClass">
            <span class="px-4 font-weight-bold">{{title}}</span>
            <span>{{message}}</span>
        </div>
    </template>
  </v-alert>
</template>

<script>
export default {
  name: "hux-alert",

  props: {
    type: {
      type: String,
      required: false,
      default: null,
    },

    message: {
      type: String,
      required: false,
      default: null,
    },

    title: {
      type: String,
      required: false,
      default: null,
    },

  },

  computed: {
    icon() {
      if( this.type=="success"){
        return "mdi-check-circle";
      }
      else if( this.type=="error") {
        return "mdi-alert-circle";
      }
      else if( this.type=="secondary") {
        return "mdi-message-alert";
      }
      else if( this.type=="primary") {
        return "mdi-information";
      }
    },
    typeClass() {
      return `${this.type}--text`;
    }
  },

}
</script>
