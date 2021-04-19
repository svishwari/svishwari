<template>
  <div class="main">
    <v-subheader> Card </v-subheader>
    <v-divider></v-divider>
    <CardInfo></CardInfo>
    <br />

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

    <v-subheader> Page Header </v-subheader>
    <v-divider></v-divider>
    <PageHeader title="Welcome back, User!" icon="mdi-bullhorn-outline">
      <template slot="description">
        <div>
          Hux is here to help you make better, faster decisions to improve your
          Customer Experiences.
          <a>Learn More ></a>
        </div>
      </template>
    </PageHeader>
    <br />
    
  </div>
</template>

<script>
import CardInfo from "@/components/common/CardInfo"
import TextField from "@/components/common/TextField"
import Button from "@/components/common/Button"
import DropdownMenu from "@/components/common/DropdownMenu"
import PageHeader from "@/components/PageHeader"

export default {
  name: "CommonComponent",
  components: {
    CardInfo,
    TextField,
    Button,
    DropdownMenu,
    PageHeader
  },
}
</script>
<style lang="scss" scoped>
.main {
  margin: 10px;
}
</style>
