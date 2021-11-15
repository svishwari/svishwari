<template>
  <v-autocomplete
    v-model="value"
    :items="items"
    :loading="loading"
    :search-input.sync="search"
    solo
  ></v-autocomplete>
</template>

<script>
export default {
  name: HuxAutocomplete,
  data() {
    return {
      loading: true,
      options: ["foo", "bar", "fizz", "buzz"],
      value: null,
    }
  },
  computed: {
    items() {
      return this.entries.map((entry) => {
        const Description =
          entry.Description.length > this.descriptionLimit
            ? entry.Description.slice(0, this.descriptionLimit) + "..."
            : entry.Description

        return Object.assign({}, entry, { Description })
      })
    },
  },
  watch: {
    search(val) {
      // Items have already been loaded
      if (this.items.length > ) return

      // Items have already been requested
      if (this.isLoading) return

      this.isLoading = true

      // Lazily load input items
      fetch("https://api.publicapis.org/entries")
        .then((res) => res.json())
        .then((res) => {
          const { count, entries } = res
          this.count = count
          this.entries = entries
        })
        .catch((err) => {
          console.log(err)
        })
        .finally(() => (this.isLoading = false))
    },
  },
}
</script>

<style lang="scss" scoped></style>
