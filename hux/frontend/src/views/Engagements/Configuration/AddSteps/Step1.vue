<template>
  <div class="eng-step-1">
    <v-row class="pt-2">
      <v-col>
        <text-field
          v-model="value.name"
          label-text="Engagement name"
          placeholder="Give this engagement a name"
          :rules="[(value) => !!value || 'Engagement name is required']"
          :error-messages="errorMessages"
          required
          data-e2e="engagement-name"
          @blur="errorMessages = []"
        />
      </v-col>
      <v-col>
        <text-field
          v-model="value.description"
          label-text="Description"
          placeholder="What is the purpose of this engagement?"
          data-e2e="engagement-description"
        />
      </v-col>
    </v-row>
  </div>
</template>

<script>
//Components
import TextField from "@/components/common/TextField.vue"

export default {
  name: "Step1",

  components: {
    TextField,
  },

  props: {
    value: {
      type: Object,
      required: true,
    },
  },

  data() {
    return {
      errorMessages: [],
    }
  },
}
</script>

<style lang="scss" scoped>
.eng-step-1 {
  margin-right: 16px;
}
</style>
