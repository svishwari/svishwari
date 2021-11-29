<template>
    <div class="rounded-sm lookalikes-overview box-shadow-none">
        <div class="header d-flex px-3 py-3">
                <span class="float-left"> Lookalikes </span>
                <v-spacer> </v-spacer>
                <span class="float-right"> 
                    <hux-icon type="plus" :size="12" color="primary" class="mr-4 mb-2" />
                    <hux-icon type="destination" :size="24" color="primary" class="mr-2" /> 
                </span>
        </div>
        <div class="lookialike-destination mx-6 my-6">
            <v-card class="rounded-sm status-card mr-2 box-shadow-none">
                <v-card-title class="d-flex pa-2">
                    <logo type="facebook" :size="22"></logo>
                    <span class="mx-2 float-left"> Facebook </span>
                </v-card-title>
                <v-list dense class="" :height="52">
                    <v-list-item>
                        Destination
                    </v-list-item>
                </v-list>
            </v-card>
        </div> 
        <div class="lookialike-destination mx-6 my-6">
            <v-card class="rounded-sm status-card mr-2 box-shadow-none">
                <v-card-title class="d-flex pa-2">
                    <logo type="facebook" :size="22"></logo>
                    <span class="mx-2"> Facebook </span>
                </v-card-title>
                <v-list dense class="" :height="52">
                    <v-list-item>
                        Destination
                    </v-list-item>
                </v-list>
            </v-card>
        </div>   
    </div>
</template>

<script>
import HuxIcon from "@/components/common/Icon.vue"
import Logo from "@/components/common/Logo.vue"

export default {
  name: "Lookalikes",
  components: { HuxIcon, Logo },
  props: {
    
  },
  data() {
    return {
      
    }
  },
  computed: {
  },
}
</script>

<style lang="scss" scoped>
.lookalikes-overview {
    .header {
        height: 40px;
    }
    .lookialike-destination {
        .rounded-sm {
            border: 1px solid #E2EAEC;
            border-radius: 12px !important;
            .v-card__title {
                background: #F9FAFB;
            }
        }
    }
}
</style>
