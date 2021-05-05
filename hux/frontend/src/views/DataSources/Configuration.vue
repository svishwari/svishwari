<template>
  <div class="add-data-source--wrap">
    <drawer v-model="localDrawer" @onClose="closeAddDataSource">
      <template v-slot:header-left>
        <div class="d-flex align-baseline">
          <h5 class="text-h5 font-weight-light pr-2">Select a data source</h5>
        </div>
      </template>
      <template v-slot:footer-left>
        <div class="d-flex align-baseline">
          <div class="font-weight-regular">
            {{ destinations.length }} results
          </div>
        </div>
      </template>
      <template v-slot:footer-right>
        <div v-if="isDataSourceSelected" class="d-flex align-baseline">
          <huxButton
            ButtonText="Cancel"
            variant="tertiary"
            size="large"
            v-bind:isTile="true"
            class="mr-2"
            @click="closeAddDataSource"
        ></huxButton>
          <huxButton
            :ButtonText="dataSourcesBtnText"
            variant="primary"
            size="large"
            v-bind:isTile="true"
            :isDisabled="!isDataSourceSelected"
            @click="addDataSources"
          ></huxButton>
        </div>
      </template>
      <template v-slot:default>
        <div class="ma-5">
          <div class="font-weight-light">Data sources</div>
          <CardHorizontal
            v-for="(destination, index) in destinations"
            :key="destination.id"
            :title="destination.name"
            :icon="destination.type"
            :isAdded="
              destination.is_added || selectedDataSources.includes(index)
            "
            :isAvailable="destination.is_enabled"
            :isAlreadyAdded="destination.is_added"
            @click="onDataSourceClick(index)"
            class="my-3"
          />
        </div>
      </template>
    </drawer>
  </div>
</template>

<script>
import Drawer from "@/components/common/Drawer"
import huxButton from "@/components/common/huxButton"
import CardHorizontal from "@/components/common/CardHorizontal"
import { mapGetters } from "vuex"
export default {
  name: "add-data-source",
  components: {
    Drawer,
    CardHorizontal,
    huxButton,
  },

  data() {
    return {
      localDrawer: this.value,
      selectedDataSources: [],
    }
  },

  props: {
    value: {
      type: Boolean,
      required: true,
      default: false,
    },
  },

  computed: {
    ...mapGetters(["destinations"]),
    isDataSourceSelected() {
      return this.selectedDataSources.length > 0
    },
    dataSourcesBtnText() {
      return `Add ${this.selectedDataSources.length} data source` ;
    }
  },
  methods: {
    onDataSourceClick: function(index) {
      if ( this.selectedDataSources.includes(index) ) {
        let deselecteRowIndex = this.selectedDataSources.indexOf(index)
        this.selectedDataSources.splice( deselecteRowIndex , 1);
      }
      else {
        this.selectedDataSources.push(index)
      }
    },
    addDataSources: function() {
      // Make a api call here
      this.closeAddDataSource()
    },
    closeAddDataSource: function() {
      this.localDrawer = false
      this.selectedDataSources = []
    }
  },
  watch: {
    value: function () {
      this.localDrawer = this.value
    },
    localDrawer: function () {
      this.$emit("input", this.localDrawer)
      if (!this.localDrawer) {
        this.$emit("onClose")
      }
    },
  },
}
</script>
