<template>
  <page class="white" max-width="912px">
    <div class="mb-10">
      <h4 class="text-h1 black--text text--darken-4">Add an application</h4>
      <p class="text-body-1 black--text text--darken-4">
        Please fill out the information below to connect a new application.
      </p>
    </div>

    <label class="d-flex text-body-2 mb-2 black--text text--darken-4">
      Select an application
    </label>

    <div class="d-flex align-center mb-3">
      <template v-if="!(selectedApplication || customApp)">
        <hux-icon
          type="plus"
          :size="16"
          color="primary"
          class="mr-4 pe-cursor"
          @click.native="toggleDrawer()"
        />
        <hux-icon
          type="application-with-border"
          :size="32"
          color="primary"
          class="primary-border pe-cursor"
          @click.native="toggleDrawer()"
        />
        <v-btn
          text
          min-width="7rem"
          height="2rem"
          class="primary--text text-body-1"
          data-e2e="drawerToggle"
          @click.native="toggleDrawer()"
        >
          Application
        </v-btn>
      </template>
      <p v-else class="text-body-1 mb-0 d-inline-flex">
        <template v-if="customApp">
          <logo type="custom-application" :size="26" />
          <span class="pl-2"> Custom Application </span>
        </template>
        <template v-else>
          <logo :type="selectedApplication.type" :size="26" />
          <span class="pl-2">{{ selectedApplication.name }}</span>
        </template>
        <a
          class="pl-7 pt-1 text-body-2"
          color="primary"
          @click="toggleDrawer()"
        >
          Change
        </a>
      </p>
    </div>

    <!-- add application form -->
    <v-form v-if="customApp">
      <v-row class="h-80 mt-4">
        <v-col>
          <label class="mb-1">Application category</label>
          <hux-dropdown
            :label="newAppDetails['category']"
            :selected="newAppDetails['category']"
            :items="categoryOptions"
            min-width="240"
            @on-select="onSelectMenuItem"
          />
        </v-col>
      </v-row>

      <v-row class="h-80">
        <v-col>
          <text-field
            v-model="newAppDetails['name']"
            label-text="Application name"
            placeholder-text="Text"
            required
            :rules="[rules.required]"
            input-type="text"
            height="40"
            class="application-field"
          />
        </v-col>
      </v-row>

      <v-row class="h-80">
        <v-col>
          <text-field
            v-model="newAppDetails['url']"
            label-text="Application URL"
            placeholder-text="www.example.com"
            required
            :rules="[rules.required]"
            input-type="text"
            height="40"
          />
        </v-col>
      </v-row>
    </v-form>
    <v-form v-if="customApp == false" class="pt-3">
      <div
        class="
          primary
          lighten-1
          border-all
          black--border
          border--lighten-2
          pa-6
          rounded
          h-106
          border-radius-12
        "
      >
        <v-row>
          <v-col>
            <text-field
              v-model="newAppDetails['url']"
              label-text="Application URL"
              placeholder-text="www.example.com"
              required
              :rules="[rules.required]"
              input-type="text"
              height="40"
            />
          </v-col>
        </v-row>
      </div>
    </v-form>

    <hux-footer slot="footer" max-width="850px" data-e2e="footer">
      <template #left>
        <hux-button
          size="large"
          variant="white"
          is-tile
          class="
            text-button
            ml-auto
            primary--text
            mr-3
            btn-border
            box-shadow-none
          "
          data-e2e="cancel-application-request"
          @click="cancel()"
        >
          Cancel &amp; return
        </hux-button>
      </template>
      <template #right>
        <hux-button
          variant="primary"
          size="large"
          :is-tile="true"
          :is-disabled="customApp == null"
          @click="add()"
        >
          Add &amp; return
        </hux-button>
      </template>
    </hux-footer>

    <drawer v-model="drawer">
      <template #header-left>
        <div class="d-flex align-center">
          <hux-icon
            type="application-with-border"
            :size="32"
            class="mr-3 black-border"
            color="black"
          />
          <h2 class="text-h2 pr-2 black--text text--lighten-4">
            Select an application
          </h2>
        </div>
      </template>
      <template #footer-left>
        <div class="d-flex align-baseline">
          <span class="text-body-2 black--text text--lighten-4">
            {{ allApplications.length }} results
          </span>
        </div>
      </template>
      <template #default>
        <div class="ma-3 font-weight-light px-6">
          <div
            v-for="(value, category, index) in groupByCategory(allApplications)"
            :key="`active-${index}`"
          >
            <label
              class="d-block text-body-2 black--text text--lighten-4 mb-2 mt-6"
            >
              {{ formatText(category) }}
            </label>

            <card-horizontal
              v-for="application in value"
              :key="application.id"
              :title="application.name"
              :icon="application.type"
              :is-added="application.is_added || isSelected(application.id)"
              :is-already-added="application.is_added"
              class="mb-2"
              data-e2e="applicationsDrawer"
              @click="onAddApplication(application.id)"
            />
          </div>
          <div>
            <v-divider class="black--border border--lighten-2 mt-8 pb-2" />

            <label
              class="d-block text-body-2 black--text text--lighten-4 mb-2 mt-6"
            >
              Uncategorized
            </label>

            <card-horizontal
              title="Request an application not on the list"
              icon="custom-application"
              :is-added="false"
              :is-already-added="false"
              requested-button
              class="mb-2"
              data-e2e="applicationsDrawer"
              @click="onAddApplication(null)"
            />
          </div>
        </div>
      </template>
    </drawer>
    <confirm-modal
      v-model="showConfirmModal"
      icon="leave-config"
      title="You are about to leave the configuration process"
      right-btn-text="Yes, leave configuration"
      body=" Are you sure you want to stop the configuration and go to another page? You will not be able to recover it and will need to start the process again."
      @onCancel="showConfirmModal = false"
      @onConfirm="navigateAway()"
    />
  </page>
</template>

<script>
import CardHorizontal from "@/components/common/CardHorizontal"
import ConfirmModal from "@/components/common/ConfirmModal.vue"
import Drawer from "@/components/common/Drawer"
import huxButton from "@/components/common/huxButton"
import HuxFooter from "@/components/common/HuxFooter"
import HuxIcon from "@/components/common/Icon.vue"
import Logo from "@/components/common/Logo"
import TextField from "@/components/common/TextField"
import Page from "@/components/Page"
import { formatText, groupBy } from "@/utils"
import sortBy from "lodash/sortBy"
import { mapActions, mapGetters } from "vuex"
import HuxDropdown from "@/components/common/HuxDropdown.vue"
import categories from "./categories.json"

export default {
  name: "AddApplication",

  components: {
    Page,
    Drawer,
    CardHorizontal,
    HuxFooter,
    huxButton,
    TextField,
    Logo,
    ConfirmModal,
    HuxIcon,
    HuxDropdown,
  },

  data() {
    return {
      loading: false,
      drawer: false,
      selectedApplicationId: null,
      selectedApplicationNotListed: null,
      authenticationDetails: {},
      isValidated: false,
      isValidating: false,
      validationError: null,
      isAddFormValid: false,
      newAppDetails: {
        category: "Uncategorized",
        name: null,
        url: null,
      },
      rules: {
        required: (value) => !!value || "This is a required field",
        validEmail: (value) =>
          /.+@.+\..+/.test(value) || "Please enter a valid email address",
      },
      selectedDataExtension: {},
      dataExtensions: [],
      showConfirmModal: false,
      navigateTo: false,
      flagForModal: false,
      ApplicationUrl: null,
      categoryOptions: categories.options,
      customApp: null,
    }
  },

  computed: {
    ...mapGetters({
      applications: "application/list",
      addedApplications: "application/addedList",
    }),

    allApplications() {
      return this.applications.map((obj) => {
        const index = this.addedApplications.findIndex(
          (el) => el["id"] == obj["id"]
        )
        return index !== -1 ? this.addedApplications[index] : obj
      })
    },

    selectedApplication() {
      return this.selectedApplicationId
        ? this.applications.find((x) => x.id == this.selectedApplicationId)
        : null
    },

    showUncategorizedAddForm() {
      return Boolean(!this.selectedApplicationId)
    },

    showCategorizedAddForm() {
      return Boolean(this.selectedApplicationId)
    },
  },

  beforeRouteLeave(to, from, next) {
    if (this.flagForModal == false) {
      this.showConfirmModal = true
      this.navigateTo = to
    } else {
      next()
    }
  },

  async mounted() {
    this.loading = true

    if (this.$route.query.select) {
      this.drawer = true
    }
    await this.getApplications()
    await this.getAddedApplications()
    this.loading = false
  },

  methods: {
    ...mapActions({
      getAddedApplications: "application/getAddedApplications",
      getApplications: "application/getApplications",
      createApplication: "application/createApplication",
      updateApplication: "application/updateApplications",
    }),
    onSelectMenuItem(item) {
      if (this.newAppDetails["category"] == item.name) {
        this.newAppDetails["category"] = "Uncategorized"
      } else {
        this.newAppDetails["category"] = item.name
      }
    },
    navigateAway() {
      this.showConfirmModal = false
      this.flagForModal = true
      this.$router.push(this.navigateTo)
    },

    toggleDrawer() {
      this.drawer = !this.drawer
    },

    isSelected(id) {
      return this.selectedApplication && this.selectedApplication.id === id
    },

    groupByCategory(list) {
      return groupBy(sortBy(list, ["category", "name"]), "category")
    },

    onAddApplication(id) {
      if (!id) {
        this.newAppDetails = {
          category: "Uncategorized",
          name: null,
          url: null,
        }
        this.customApp = true
      } else {
        let application = this.applications.find((item) => item.id == id)

        this.newAppDetails = {
          url: application.url,
        }
        this.customApp = false
      }
      this.selectedApplicationId = id
      this.drawer = false
    },

    async add() {
      try {
        if (!this.selectedApplicationId) {
          await this.createApplication(this.newAppDetails)
        } else if (this.selectedApplicationId) {
          await this.updateApplication({
            id: this.selectedApplicationId,
            data: this.newAppDetails,
          })
        }
        this.flagForModal = true
        this.$router.back()
      } catch (error) {
        console.error(error)
      }
    },

    cancel() {
      this.flagForModal = true
      this.$router.back()
    },
    formatText: formatText,
  },
}
</script>

<style lang="scss" scoped>
.h-80 {
  height: 80px;
}
.hux-dropdown {
  ::v-deep .main-button {
    margin: 0px !important;
  }
}
.primary-border {
  border-radius: 50%;
  border: 1px solid var(--v-primary-base);
  box-shadow: 1.5px 1.5px 5px rgba(57, 98, 134, 0.15);
}
.black-border {
  border-radius: 50%;
  border: 0.5px solid var(--v-black-base);
}
.pe-cursor {
  pointer-events: cursor;
}
.select-menu-class {
  .v-select-list {
    ::v-deep .v-list-item__title {
      font-size: 16px;
    }
  }
}
.h-106 {
  height: 110px;
}
.border-radius-12 {
  border-radius: 12px !important;
}
</style>
