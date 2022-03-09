<template>
  <page-header :header-height="110">
    <template #left>
      <div>
        <breadcrumb :items="items" />
      </div>
      <div class="text-subtitle-1 font-weight-regular">
        Measure the signals of trust, predict how trust sentiment will impact
        customer & employee behaviors, and identify actions to (re)build trust.
      </div>
    </template>
  </page-header>
</template>

<script>
import PageHeader from "@/components/PageHeader"
import Breadcrumb from "@/components/common/Breadcrumb"
export default {
  name: "TrustID",
  components: {
    PageHeader,
    Breadcrumb,
  },
  data() {
    return {
      items: [
        {
          text: "HX TrustID",
          disabled: true,
          href: "/trust-id",
          icon: "trust-id",
        },
      ],
    }
  },
}
</script>

<style lang="scss" scoped></style>
