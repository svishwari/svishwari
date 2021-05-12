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
            {{ dataSources.length }} results
          </div>
        </div>
      </template>
      <template v-slot:footer-right>
        <div v-if="isDataSourcesSelected" class="d-flex align-baseline">
          <huxButton
            ButtonText="Cancel"
            variant="tertiary"
            size="large"
            :isTile="true"
            class="mr-2"
            @click="closeAddDataSource"
          ></huxButton>
          <huxButton
            :ButtonText="dataSourcesBtnText"
            variant="primary"
            size="large"
            :isTile="true"
            :isDisabled="!isDataSourcesSelected"
            @click="addDataSources"
          ></huxButton>
        </div>
      </template>
      <template v-slot:default>
        <div class="ma-5">
          <div class="font-weight-light">Data sources</div>
          <CardHorizontal
            v-for="dataSource in dataSources"
            :key="dataSource.id"
            :title="dataSource.name"
            :icon="dataSource.type"
            :isAdded="
              dataSource.is_added ||
              selectedDataSourceIds.includes(dataSource.id)
            "
            :isAvailable="dataSource.is_enabled"
            :isAlreadyAdded="dataSource.is_added"
            @click="onDataSourceClick(dataSource.id)"
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
// import { mapGetters } from "vuex"
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
      selectedDataSourceIds: [],
      dataSources: [],
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
    // ...mapGetters({
    //   TODO get datasources list from api
    //   dataSources: "destinations/list",
    // }),

    isDataSourcesSelected() {
      return this.selectedDataSourceIds.length > 0
    },
    dataSourcesBtnText() {
      let count = this.selectedDataSourceIds.length
      return `Add ${count} data source${count > 1 ? "s" : ""}`
    },
  },
  methods: {
    onDataSourceClick: function (id) {
      if (this.selectedDataSourceIds.includes(id)) {
        const deselectedId = this.selectedDataSourceIds.indexOf(id)
        this.selectedDataSourceIds.splice(deselectedId, 1)
      } else {
        this.selectedDataSourceIds.push(id)
      }
    },
    addDataSources: function () {
      // Make a api call here
      this.closeAddDataSource()
    },
    closeAddDataSource: function () {
      this.localDrawer = false
      this.selectedDataSourceIds = []
    },
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
