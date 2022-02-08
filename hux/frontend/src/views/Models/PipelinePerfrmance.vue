<template>
  <div class="pipeline-tab-wrap">
    <v-card class="mt-5 rounded-lg pt-5 pb-6 pl-6 pr-6 box-shadow-5">
      <v-card-title class="d-flex justify-space-between pa-0 pr-2">
        <h3 class="text-h3 mb-2 black--text text--darken-4">Training</h3>
      </v-card-title>

      <v-row class="mt-1" col="12">
        <v-col md="2">
          <div class="pipeline__card pa-4">
            <label class="text-body-2 black--text text--lighten-4 ma-0">
              Run frequency
            </label>
            <p
              class="
                mt-1
                caption
                black--text
                text--darken-4
                font-weight-semi-bold
                ma-0
              "
            >
              {{ runDurationData.training.frequency | Empty("-") }}
            </p>
          </div>
        </v-col>
        <v-col md="2" class="card-space">
          <div class="pipeline__card pa-4">
            <label class="text-body-2 black--text text--lighten-4 ma-0">
              Last run
            </label>
            <p
              class="
                mt-1
                caption
                black--text
                text--darken-4
                font-weight-semi-bold
                ma-0
              "
            >
              {{
                runDurationData.training.last_run
                  | Date("MM/DD/YY [•] h:mm A")
                  | Empty("-")
              }}
            </p>
          </div>
        </v-col>
        <v-col md="2" class="card-space">
          <div class="pipeline__card pa-4">
            <label class="text-body-2 black--text text--lighten-4 ma-0">
              Most recent run duration
            </label>
            <tooltip>
              <template #label-content>
                <p
                  class="
                    mt-1
                    caption
                    black--text
                    text--darken-4
                    font-weight-semi-bold
                    ma-0
                  "
                >
                  {{
                    runDurationData.training.most_recent_run_duration
                      | Empty("-")
                  }}
                </p>
              </template>
              <template #hover-content> HH:MM:SS </template>
            </tooltip>
          </div>
        </v-col>
        <v-col md="3" class="card-space">
          <div class="pipeline__card pa-4">
            <label class="text-body-2 black--text text--lighten-4 ma-0">
              Status (last 10)
            </label>
            <br />
            <span
              v-for="(data, index) in runDurationData.training.run_duration"
              :key="data.timestamp"
            >
              <tooltip>
                <template #label-content>
                  <span
                    class="mt-2 mr-2"
                    :class="data.status === 'Success' ? 'greenDot' : 'redDot'"
                  ></span>
                </template>
                <template #hover-content>
                  <div
                    class="mt-1 mb-1 text--body- black--text text--base ma-0"
                  >
                    {{ index + 1 }} of last
                    {{ runDurationData.training.run_duration.length }} runs
                    <div>
                      <span
                        class="mt-1 mr-1"
                        :class="
                          data.status === 'Success' ? 'greenDot' : 'redDot'
                        "
                      ></span>
                      <span class="mt-n2">{{ data.status }} </span>
                    </div>
                    <div class="mt-1">
                      {{
                        runDurationData.training.last_run
                          | Date("MM/DD/YY h:mm A")
                          | Empty("-")
                      }}
                    </div>
                  </div>
                </template>
              </tooltip>
            </span>
          </div>
        </v-col>
        <v-col md="2" class="card-space">
          <div class="pipeline__card pa-4">
            <label class="text-body-2 black--text text--lighten-4 ma-0">
              Total runs
            </label>
            <p
              class="
                mt-1
                caption
                black--text
                text--darken-4
                font-weight-semi-bold
                ma-0
              "
            >
              {{ runDurationData.training.total_runs | Empty("-") }}
            </p>
          </div>
        </v-col>
      </v-row>
      <div class="pt-6">
        <div class="card-border pa-6">
          <span class="d-flex mb-2">
            <h3 class="text-h3">Run duration (last 10)</h3>
          </span>
          <run-duration-chart
            :runDurationData="runDurationData.training.run_duration"
          />
        </div>
      </div>
    </v-card>
    <v-card class="mt-6 rounded-lg pt-5 pb-6 pl-6 pr-6 box-shadow-5">
      <v-card-title class="d-flex justify-space-between pa-0 pr-2">
        <h3 class="text-h3 mb-2 black--text text--darken-4">Scoring</h3>
      </v-card-title>

      <v-row class="mt-1" col="12">
        <v-col md="2">
          <div class="pipeline__card pa-4">
            <label class="text-body-2 black--text text--lighten-4 ma-0">
              Run frequency
            </label>
            <p
              class="
                mt-1
                caption
                black--text
                text--darken-4
                font-weight-semi-bold
                ma-0
              "
            >
              {{ runDurationData.training.frequency | Empty("-") }}
            </p>
          </div>
        </v-col>
        <v-col md="2" class="card-space">
          <div class="pipeline__card pa-4">
            <label class="text-body-2 black--text text--lighten-4 ma-0">
              Last run
            </label>
            <p
              class="
                mt-1
                caption
                black--text
                text--darken-4
                font-weight-semi-bold
                ma-0
              "
            >
              {{
                runDurationData.training.last_run
                  | Date("MM/DD/YY [•] h:mm A")
                  | Empty("-")
              }}
            </p>
          </div>
        </v-col>
        <v-col md="2" class="card-space">
          <div class="pipeline__card pa-4">
            <label class="text-body-2 black--text text--lighten-4 ma-0">
              Most recent run duration
            </label>
            <p
              class="
                mt-1
                caption
                black--text
                text--darken-4
                font-weight-semi-bold
                ma-0
              "
            >
              {{
                runDurationData.training.most_recent_run_duration | Empty("-")
              }}
            </p>
          </div>
        </v-col>
        <v-col md="3" class="card-space">
          <div class="pipeline__card pa-4">
            <label class="text-body-2 black--text text--lighten-4 ma-0">
              Status (last 10)
            </label>
            <br />
            <span
              v-for="(data, index) in runDurationData.scoring.run_duration"
              :key="data.timestamp"
            >
              <tooltip>
                <template #label-content>
                  <span
                    class="mt-2 mr-2"
                    :class="data.status === 'Success' ? 'greenDot' : 'redDot'"
                  ></span>
                </template>
                <template #hover-content>
                  <div
                    class="mt-1 mb-1 text--body- black--text text--base ma-0"
                  >
                    {{ index + 1 }} of last
                    {{ runDurationData.scoring.run_duration.length }} runs
                    <div>
                      <span
                        class="mt-1 mr-1"
                        :class="
                          data.status === 'Success' ? 'greenDot' : 'redDot'
                        "
                      ></span>
                      <span class="mt-n2">{{ data.status }} </span>
                    </div>
                    <div class="mt-1">
                      {{
                        runDurationData.training.last_run
                          | Date("MM/DD/YY h:mm A")
                          | Empty("-")
                      }}
                    </div>
                  </div>
                </template>
              </tooltip>
            </span>
          </div>
        </v-col>
        <v-col md="2" class="card-space">
          <div class="pipeline__card pa-4">
            <label class="text-body-2 black--text text--lighten-4 ma-0">
              Total runs
            </label>
            <p
              class="
                mt-1
                caption
                black--text
                text--darken-4
                font-weight-semi-bold
                ma-0
              "
            >
              {{ runDurationData.training.total_runs | Empty("-") }}
            </p>
          </div>
        </v-col>
      </v-row>
      <div class="pt-6">
        <div class="card-border pa-6">
          <span class="d-flex mb-2">
            <h3 class="text-h3">Run duration (last 10)</h3>
          </span>
          <run-duration-chart
            :runDurationData="runDurationData.scoring.run_duration"
          />
        </div>
      </div>
    </v-card>
  </div>
</template>
<script>
import runDurationData from "@/api/mock/fixtures/runDurationData.js"
import RunDurationChart from "@/components/common/RunDurationChart/RunDurationChart"
import Tooltip from "@/components/common/Tooltip.vue"

export default {
  name: "PipelinePerfrmance",
  components: {
    RunDurationChart,
    Tooltip,
  },
  data() {
    return {
      tabOption: 0,
      runDurationData: runDurationData,
    }
  },
}
</script>
<style lang="scss" scoped>
.pipeline-tab-wrap {
  .card-border {
    border: 1px solid var(--v-black-lighten2);
    border-radius: 12px;
  }
  .pipeline__card {
    @extend .card-border;
    height: 80px;
  }
  .card-space {
    margin-left: -10px !important;
  }
}
.dots {
  margin-right: 4px;
  height: 15px;
  width: 15px;
  border-radius: 50%;
  display: inline-block;
}
.greenDot {
  @extend .dots;
  background-color: var(--v-success-base) !important;
}
.redDot {
  @extend .dots;
  background-color: var(--v-error-base) !important;
}
</style>