<template>
  <div class="main">

    <v-subheader> Card </v-subheader>
    <v-divider></v-divider>  
    <CardInfo></CardInfo>
    <br>

    <v-subheader> Text Feild </v-subheader>
    <v-divider></v-divider>
    <TextField></TextField>
    <br>


  </div>
</template>

<script>
import CardInfo from "@/components/common/CardInfo"
import TextField from "@/components/common/TextField"

export default {
  name: "CommonComponent",
  components: {
    CardInfo,
    TextField,
  },
}
</script>
<style lang="scss" scoped>
.main {
    margin: 10px;
}
</style>