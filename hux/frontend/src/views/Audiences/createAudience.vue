<template>
  <div class="create-audience-wrap">
    <PageHeader>
      <template slot="left">
        <Breadcrumb :items="breadcrumbItems" />
      </template>
    </PageHeader>
    <div class="mt-10 ml-15">
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
    </div>

    <div class="timeline-wrapper mt-9 ml-9">
      <v-timeline align-top dense class="">
        <v-timeline-item color="blue" class="timeline-section">
          <template v-slot:icon class="timeline-icon-section">
            <span>1</span>
          </template>
          <v-row class="pt-1">
            <v-col cols="4">
              <strong>General information</strong>
              <TextField
                placeholderText="What is the name for this audience ?"
                labelText="Audience name"
                backgroundColor="white"
                v-bind:required="true"
                class="mt-1"
              ></TextField>
            </v-col>
            <v-col cols="8">
              <div class="mt-8 ml-15">
                Attach an engagement (we can auto-create an engagement for you)
                - you must have at least one
              </div>
            </v-col>
          </v-row>
        </v-timeline-item>
        <v-timeline-item color="blue" class="timeline-section">
          <template v-slot:icon class="timeline-icon-section">
            <span>2</span>
          </template>
          <v-row class="pt-1">
            <v-col cols="12">
              <strong
                >Attributes selection (you can always do this later !)</strong
              >
            </v-col>
          </v-row>
        </v-timeline-item>
        <v-timeline-item color="blue" class="timeline-section">
          <template v-slot:icon class="timeline-icon-section">
            <span>3</span>
          </template>
          <v-row class="pt-1">
            <v-col cols="12">
              <strong
                >Select a destination (you can add more than one) -
                optional</strong
              >
            </v-col>
          </v-row>
        </v-timeline-item>
      </v-timeline>

      <Footer absolute padless color="white" class="footer">
        <template v-slot:left>
          <huxButton
            ButtonText="Cancel"
            variant="tertiary"
            v-bind:isTile="true"
            width="94"
            height="40"
            class="ma-2"
            @click.native="$router.go(-1)"
          ></huxButton>
          <huxButton
            ButtonText="Save &amp; complete later"
            variant="tertiary"
            v-bind:isTile="true"
            width="201"
            height="40"
            class="ma-2"
          ></huxButton>
        </template>
        <template v-slot:right>
          <huxButton
            ButtonText="Create"
            variant="primary"
            v-bind:isTile="true"
            width="94"
            height="44"
            class="ma-2"
          ></huxButton>
        </template>
      </Footer>
    </div>
  </div>
</template>

<script>
import PageHeader from "@/components/PageHeader"
import Breadcrumb from "@/components/common/Breadcrumb"
import MetricCard from "@/components/common/MetricCard"
import Footer from "@/components/common/Footer"
import huxButton from "@/components/common/huxButton"
import TextField from "@/components/common/TextField"

export default {
  name: "createAudience",
  components: {
    MetricCard,
    Footer,
    huxButton,
    PageHeader,
    Breadcrumb,
    TextField,
  },
  data() {
    return {
      breadcrumbItems: [
        {
          text: "Audiences",
          disabled: false,
          href: "/" + this.$route.path.split("/")[1],
          icon: "mdi-flip-h mdi-account-plus-outline",
        },
        {
          text: "Create audiences",
          disabled: false,
          href: this.$route.path,
          icon: "mdi-flip-h mdi-account-plus-outline",
        },
      ],
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
    box-shadow: 0px -0.5px 5px 1px rgba(0, 0, 0, 0.15) !important;
  }
  ::v-deep .timeline-wrapper {
    .theme--light.v-timeline:before {
      border: 1px dashed #00A3E0;
    }
    .theme--light.v-timeline-item {
      .v-timeline-item__divider {
        .v-timeline-item__dot {
          background: #00A3E0;
          .v-timeline-item__inner-dot {
            background-color: white !important;
            color: #00A3E0;
          }
        }
      }
    }
  }
}
</style>
