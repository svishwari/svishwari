<template>
  <div>
    <v-menu v-model="openMenu" :min-width="192" left offset-y close-on-click>
      <template #activator="{ on }">
        <span
          class="d-flex cursor-pointer mr-4"
          data-e2e="application-dropdown"
          v-on="on"
          @click="addedApplications()"
        >
          <tooltip class="tooltip-application" :z-index="99">
            <template #label-content>
              <span :class="{ 'icon-shadow': openMenu }">
                <icon
                  class="mx-2 my-2 nav-icon"
                  type="application"
                  :size="24"
                  :class="{ 'active-icon': openMenu }"
                />
              </span>
            </template>
            <template #hover-content> Application </template>
          </tooltip>
        </span>
      </template>
      <v-list>
        <v-list-item>
          <v-list-item-title
            class="font-weight-semi-bold text-subtitle-1 view-all mt-2 mb-3"
          >
            Applications
          </v-list-item-title>
        </v-list-item>
        <span v-for="(item, index) in getDropdownOptions" :key="index">
          <v-list-item
            v-if="item.isVisible"
            :disabled="item.isDisabled"
            class="view-all"
            data-e2e="application-options"
          >
            <v-list-item-title
              v-if="!item.menu"
              @click="item.onClick && item.onClick(data)"
            >
              {{ item.title }}
            </v-list-item-title>

            <v-menu
              v-else
              v-model="isSubMenuOpen"
              offset-x
              nudge-right="16"
              nudge-top="4"
              left
              nudge-left="45"
              min-width="300"
              z-index="8"
              content-class="app-menu"
            >
              <template #activator="{ on, attrs }">
                <v-list-item-title v-bind="attrs" v-on="on">
                  {{ item.title }}
                  <v-icon> mdi-chevron-right </v-icon>
                </v-list-item-title>
              </template>
              <template #default>
                <span v-for="(category, key) in getCategories" :key="key">
                  <v-list-item
                    v-if="
                      item.menu.filter(
                        (x) => x.category.toUpperCase() == category
                      ).length > 0
                    "
                    class="white h-32"
                  >
                    <span class="text-body-1 black--text text--lighten-4">
                      {{ category }}
                    </span>
                  </v-list-item>
                  <v-list-item
                    v-for="(app, ind) in item.menu.filter(
                      (x) => x.category.toUpperCase() == category
                    )"
                    :key="ind"
                    :disabled="app.isDisabled"
                    class="white h-32 view-all sub-menu-class px-3"
                  >
                    <v-list-item-title
                      class="d-flex text-body-1"
                      @click="app.onClick && app.onClick()"
                    >
                      <logo v-if="app.icon" :size="24" :type="app.icon" />
                      <span class="ml-1 mt-half">{{ app.title }}</span>
                    </v-list-item-title>
                    <span
                      class="d-none delete-button"
                      @click="app.onDelete && app.onDelete()"
                    >
                      <icon :size="18" type="delete-button" color="darkD" />
                    </span>
                  </v-list-item>
                </span>
              </template>
            </v-menu>
          </v-list-item>
        </span>
      </v-list>
    </v-menu>
    <confirm-modal
      v-model="showConfirmModal"
      icon="sad-face"
      type="error"
      title="You are about to remove"
      :sub-title="selectedAppName"
      right-btn-text="Remove"
      left-btn-text="Cancel"
      data-e2e="remove-application-confirmation"
      body="Are you sure you want to remove this application shortcut?"
      @onCancel="showConfirmModal = !showConfirmModal"
      @onConfirm="deleteApplication()"
    >
    </confirm-modal>
  </div>
</template>

<script>
import ConfirmModal from "@/components/common/ConfirmModal"
import Tooltip from "./common/Tooltip.vue"
import Icon from "@/components/common/Icon"
import Logo from "@/components/common/Logo"
import { mapGetters, mapActions } from "vuex"

export default {
  name: "Application",
  components: {
    Tooltip,
    Icon,
    Logo,
    ConfirmModal,
  },

  data() {
    return {
      openMenu: null,
      isSubMenuOpen: null,
      showConfirmModal: false,
      selectedId: null,
    }
  },

  computed: {
    ...mapGetters({
      applicationList: "application/addedList",
    }),
    selectedAppName() {
      return (
        this.selectedId &&
        this.applicationList.find((x) => x.id == this.selectedId).name
      )
    },
    getDropdownOptions() {
      return [
        {
          title: "Open an application",
          isDisabled: false,
          isVisible: this.applicationList.length > 0,
          menu: this.applicationList.map((item) => {
            return {
              id: item.id,
              title: item.name,
              category: item.category,
              icon: item.type,
              isDisabled: false,
              onClick: () => window.open("https://" + item.url),
              onDelete: () => this.removeApplication(item.id),
            }
          }),
        },
        {
          title: "Add an application",
          isDisabled: false,
          isVisible: true,
          onClick: () => this.addApplication(),
        },
      ]
    },
    getCategories() {
      return Array.from(
        new Set(this.applicationList.map((x) => x.category.toUpperCase()))
      ).sort()
    },
  },

  watch: {
    isSubMenuOpen(newValue) {
      this.openMenu = newValue
    },
  },

  methods: {
    ...mapActions({
      addedApplications: "application/getAddedApplications",
    }),

    addApplication() {
      this.$router.push({
        name: "AddApplication",
      })
    },

    removeApplication(id) {
      this.selectedId = id
      this.showConfirmModal = true
    },

    async deleteApplication() {
      this.showConfirmModal = false
      await this.$store.dispatch("application/updateApplications", {
        id: this.selectedId,
        data: {
          is_added: false,
        },
      })
      this.selectedId = null
    },
  },
}
</script>

<style lang="scss" scoped>
.v-menu__content {
  top: 70px !important;
  margin-left: 8px !important;
  .v-list {
    .v-list-item {
      min-height: 32px !important;
    }
  }
}
.h-32 {
  min-height: 32px !important;
}
.view-all {
  @extend .cursor-pointer;
  &:hover {
    background-color: var(--v-primary-lighten1);
  }
}
.delete-button {
  margin-left: auto;
}
.sub-menu-class:hover {
  background: var(--v-primary-lighten1);
}
.sub-menu-class:hover .delete-button {
  display: block !important;
}
.mt-half {
  margin-top: 2px;
}
.app-menu {
  top: 118px !important;
}
</style>
