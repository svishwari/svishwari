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
      <!-- <MetricCard
        class="list-item mr-3"
        :width="135"
        :height="80"
        v-for="(item, i) in overviewListItems"
        :key="i"
        :title="item.title"
        :subtitle="item.subtitle"
        :icon="item.icon"
        :active="true"
      ></MetricCard> -->
    </div>
    <v-divider class="divider mt-5"></v-divider>
  </div>
</template>

<script>
// import MetricCard from "@/components/common/MetricCard"

export default {
  name: "createAudience",
  components: {
    // MetricCard,
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
}
</style>
