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

    <v-subheader> Button </v-subheader>
    <v-divider></v-divider>
    <Button></Button>
    <br>

    <v-subheader> Select Dropdown </v-subheader>
    <v-divider></v-divider>
    <DropdownMenu></DropdownMenu>
    <br>


  </div>
</template>

<script>
import CardInfo from "@/components/common/CardInfo"
import TextField from "@/components/common/TextField"
import Button from "@/components/common/Button"
import DropdownMenu from "@/components/common/DropdownMenu"

export default {
  name: "CommonComponent",
  components: {
    CardInfo,
    TextField,
    Button,
    DropdownMenu
  },
}
</script>
<style lang="scss" scoped>
.main {
    margin: 10px;
}
</style>