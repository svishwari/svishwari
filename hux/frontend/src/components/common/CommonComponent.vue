<template>
  <div class="main">
    <v-subheader> Card </v-subheader>
    <v-divider></v-divider>
    <CardInfo></CardInfo>
    <br />

    <v-subheader> Text Feild </v-subheader>
    <v-divider></v-divider>
    <TextField></TextField>
    <br />

    <v-subheader> Hux Table</v-subheader>
    <v-divider></v-divider>
    <br />
    <hux-table
      :columnDef="columnDefs"
      :tableData="rowData"
      height="250px"
      hasCheckBox=true
    ></hux-table>
  </div>
</template>

<script>
import CardInfo from "@/components/common/CardInfo"
import TextField from "@/components/common/TextField"
import HuxTable from "@/components/common/huxTable.vue"

export default {
  name: "CommonComponent",
  components: {
    CardInfo,
    TextField,
    HuxTable,
  },
  data() {
    return {
      columnDefs: [
        { field: "make", sortable: true, sort:'desc' },
        { field: "model", sortable: true },
        { field: "price", sortable: true },
      ],

      rowData: [
        { make: "Toyota", model: "Celica", price: 35000 },
        { make: "Ford", model: "Mondeo", price: 32000 },
        { make: "Porsche", model: "Boxter", price: 72000 },
      ],
    }
  },
  mounted() {},
}
</script>
<style lang="scss" scoped>
.main {
  margin: 10px;
}
</style>
