<template>
  <div>
    <multi-select-list-item :disabled="disabled"></multi-select-list-item>
    <small-list-item />
    <form-list-item />
  </div>
</template>

<script>
import MultiSelectListItem from "./MultiSelectListItem.vue"
import SmallListItem from "./SmallListItem.vue"
import FormListItem from "./FormListItem.vue"

export default {
  name: "HuxList",
  components: { MultiSelectListItem, SmallListItem, FormListItem },
  props: {
    disabled: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
}
</script>
