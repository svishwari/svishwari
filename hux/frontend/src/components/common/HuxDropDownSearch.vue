<template>
  <v-menu
    v-model="localToggle"
    offset-y
    content-class="dropdown-search-wrapper"
    max-height="320"
    :close-on-content-click="false"
  >
    <template #activator="{ on }">
      <span v-on="on">
        <slot name="activator"></slot>
      </span>
    </template>
    <template #default>
      <v-text-field
        v-if="isSearchEnabled"
        v-model="searchText"
        color="neroBlack"
        class="search-field-container"
        placeholder="Search"
        prepend-icon="mdi-magnify"
      />
      <div v-for="(item, i) in filteredItems" :key="i">
        <div
          class="search-item"
          :class="{ 'search-item-selected': isItemAdded(item) !== -1 }"
          @click="toggleItem(item)"
        >
          <div class="d-flex align-center">
            <v-icon
              v-if="isItemAdded(item) !== -1"
              :size="11"
              color="primary"
              class="pr-2"
            >
              mdi-check
            </v-icon>
            <span v-if="item.type" class="pr-2">
              <logo :type="item.type" :size="21" />
            </span>
            <span class="text-h6">{{ item.name }}</span>
          </div>
        </div>
      </div>
    </template>
  </v-menu>
</template>

<script>
import Logo from "./Logo.vue"

export default {
  name: "HuxDropDownSearch",

  components: {
    Logo,
  },

  props: {
    value: {
      type: Array,
      required: true,
    },

    items: {
      type: Array,
      required: true,
    },

    toggleDropDown: {
      type: Boolean,
      required: false,
      default: false,
    },

    isSearchEnabled: {
      type: Boolean,
      required: false,
      default: true,
    },

    minSelection: {
      type: Number,
      required: false,
      default: 0,
    },
  },

  data: function () {
    return {
      localToggle: false,
      searchText: null,
    }
  },

  computed: {
    filteredItems() {
      let searchText = this.searchText ? this.searchText.toLowerCase() : ""
      return this.items.filter((each) =>
        each.name.toLowerCase().includes(searchText)
      )
    },
  },

  watch: {
    toggleDropDown(value) {
      this.localToggle = value
    },

    localToggle(value) {
      this.$emit("onToggle", value)
      if (!value) {
        this.searchText = null
      }
    },
  },

  methods: {
    toggleItem(item) {
      let itemIndex = this.isItemAdded(item)
      if (itemIndex !== -1) {
        if (this.value.length !== this.minSelection) {
          this.value.splice(itemIndex, 1)
        }
      } else {
        this.value.push(item)
      }
      this.$emit("onValueChange")
    },

    isItemAdded(item) {
      return this.value.findIndex((each) => each === item)
    },
  },
}
</script>

<style lang="scss" scoped>
.dropdown-search-wrapper {
  background-color: var(--v-white-base);
  @extend .box-shadow-25;
  ::v-deep .v-input {
    .v-input__control {
      .v-input__slot {
        margin-bottom: 0 !important;
        &::before {
          content: none;
        }
        &::after {
          content: none;
        }
        input::placeholder {
          color: var(--v-black-darken1) !important;
        }
      }
      .v-text-field__details {
        display: none;
      }
    }
  }
  .search-field-container {
    padding: 5px 15px 5px 10px;
    background-color: var(--v-primary-lighten2);
    align-items: center;
    height: 32px;
    margin-top: 0;
    ::v-deep .v-input__prepend-outer {
      margin: 0;
      .v-input__icon--prepend .v-icon {
        font-size: 16px;
        color: var(--v-black-darken4);
      }
    }
    ::v-deep .v-input__control {
      .v-input__slot {
        input::placeholder {
          color: var(--v-black-darken4) !important;
        }
      }
    }
  }
  .search-item {
    color: var(--v-black-darken4);
    padding: 5px 15px;
    @extend .cursor-pointer;
    &:hover {
      background-color: var(--v-primary-lighten1);
    }
  }
  .search-item-selected {
    color: var(--v-primary-base);
    background-color: var(--v-primary-lighten1);
  }
}
</style>
