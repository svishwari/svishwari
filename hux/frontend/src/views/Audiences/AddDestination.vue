<template>
  <diV class="add-destination-wrapper">
    Extension type
    <div class="d-flex align-center mt-2">
      <diV
        class="extension-type mr-4 text-center"
        v-bind:class="[isActive ? 'active' : '']"
        @click="toggleClass($event)"
      >
        <div class="child mt-8">
          <div class="icon">block 1</div>
          <div class="label">New data extension</div>
        </div>
      </diV>
      <diV
        class="extension-type mr-4 text-center"
        v-bind:class="[!isActive ? 'active' : '']"
        @click="toggleClass($event)"
      >
        <div class="child mt-8">
          <div class="icon">block 2</div>
          <div class="label">Existing data extension</div>
        </div>
      </diV>
    </div>

    <div class="mt-6" v-if="isActive">
      <div>
        <label class="d-flex align-items-center">
          Journey type
          <v-tooltip top>
            <template v-slot:activator="{ on, attrs }">
              <v-icon
                color="primary"
                size="small"
                class="ml-2"
                v-bind="attrs"
                v-on="on"
              >
                mdi-alert-circle-outline
              </v-icon>
            </template>
            <span> Type of journey </span>
          </v-tooltip>
        </label>
        <v-radio-group v-model="journeyType" row>
          <v-radio label="Automated (Batched)" value="radio-1"></v-radio>
          <v-radio
            label="Triggered (API) - coming soon"
            value="radio-2"
          ></v-radio>
        </v-radio-group>
      </div>
      <TextField
        v-model="Extension"
        labelText="Data extension name"
        icon="mdi-alert-circle-outline"
        placeholderText="What is the name for this new data extension?"
        helpText="Extension name"
      ></TextField>
    </div>

    <div class="mt-6" v-if="!isActive">
      <label class="d-flex align-items-center mb-2">
        Existing data extension
      </label>
    </div>
  </diV>
</template>
<script>
import TextField from "@/components/common/TextField"

export default {
  name: "AddDestination",
  components: { TextField },
  data() {
    return {
      isActive: true,
      journeyType: null,
      Extension: null,
      DropdownData: [
        { value: "1 - 25" },
        { value: "26 - 50" },
        { value: "50+" },
      ],
    }
  },
  methods: {
    toggleClass: function (event) {
      if (!event.currentTarget.classList.contains("active")) {
        this.isActive = !this.isActive
      }
    },
  },
}
</script>
<style lang="scss" scoped>
.add-destination-wrapper {
  .extension-type {
    height: 100px;
    width: 196px;
    left: 24px;
    top: 126px;
    border-radius: 4px;
    background: #ffffff;
    border: 1px solid #d0d0ce;
    box-sizing: border-box;
    &.active {
      border: 1px solid #005587;
    }
    .child {
      .label {
        color: #005587;
      }
    }
  }
}
</style>
