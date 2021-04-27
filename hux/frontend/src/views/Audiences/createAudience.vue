<template>
  <div class="create-audience-wrap mt-10 ml-15">
    <div class="heading font-weight-light">Add an audience</div>
    <div class="sub-heading font-weight-regular">
      Build a target Audience from the data you own. Feel free to save and
      complete later as a draft or simply create and fill in the information
      when you are ready.
    </div>

    <div class="overview mt-15">Audience overview</div>
    <div class="row overview-list mb-0 ml-0 mt-1">
      <MetricCard
        class="list-item mr-3"
        :width="135"
        :height="80"
        v-for="(item, i) in overviewListItems"
        :key="i"
        :title="item.title"
        :subtitle="item.subtitle"
        :icon="item.icon"
        :active="true"
      ></MetricCard>
    </div>
    <v-divider class="divider mt-5"></v-divider>

    <Footer absolute padless color="white" class="footer">
      <template v-slot:left>
        <huxButton
          ButtonText="Cancel"
          variant="tertiary"
          v-bind:isTile="true"
          width="94"
          height="40"
          @click.native="$router.go(-1)"
        ></huxButton>
        <huxButton
          ButtonText="Save &amp; complete later"
          variant="tertiary"
          v-bind:isTile="true"
          width="201"
          height="40"
        ></huxButton>
      </template>
      <template v-slot:right>
        <huxButton
          ButtonText="Create"
          variant="primary"
          v-bind:isTile="true"
          width="94"
          height="44"
        ></huxButton>
      </template>
    </Footer>
  </div>
</template>

<script>
import MetricCard from "@/components/common/MetricCard"
import Footer from "@/components/common/Footer"
import huxButton from "@/components/common/huxButton"

export default {
  name: "createAudience",
  components: {
    MetricCard,
    Footer,
    huxButton,
  },
  data() {
    return {
      overviewListItems: [
        { title: "Countries", subtitle: "2", icon: "mdi-earth" },
        { title: "US States", subtitle: "52", icon: "mdi-map" },
        { title: "Cities", subtitle: "19,495", icon: "mdi-map-marker-radius" },
        { title: "Age", subtitle: "-", icon: "mdi-cake-variant" },
        { title: "Women", subtitle: "52%", icon: "mdi-gender-female" },
        { title: "Men", subtitle: "46%", icon: "mdi-gender-male" },
        { title: "Other", subtitle: "2%", icon: "mdi-gender-male-female" },
      ],
    }
  },
}
</script>

<style lang="scss" scoped>
.create-audience-wrap {
  .heading {
    font-size: 24px;
    line-height: 40px;
  }
  .sub-heading {
    font-size: 14px;
    line-height: 22px;
    max-width: 910px;
  }
  .overview {
    font-size: 15px;
    line-height: 20px;
  }
  .divider {
    max-width: 1103px;
  }
  .footer {
    padding-left: 50px;
    box-shadow: 0px -0.5px 5px 1px rgba(0, 0, 0, 0.15) !important
  }
}
</style>
