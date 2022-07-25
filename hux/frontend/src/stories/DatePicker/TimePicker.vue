<template>
  <div class="ma-1 d-flex align-items-center">
    <span class="mt-1">Hours</span>
    <div>
      <button
        v-for="(hour, index) in Hours"
        :key="index"
        class="box ma-2"
        @click="selectHour(hour)"
      >
        {{ hour }}
      </button>
    </div>
    <span class="mt-2">Minutes</span>
    <div>
      <button
        v-for="(min, index) in Minutes"
        :key="index"
        class="box ma-2"
        @click="selectMinute(min)"
      >
        {{ min }}
      </button>
    </div>
  </div>
</template>
<script>
export default {
  name: "TimePicker",
  computed: {
    Hours() {
      return [
        "00",
        "01",
        "02",
        "03",
        "04",
        "05",
        "06",
        "07",
        "08",
        "09",
        "10",
        "11",
        "12",
      ]
    },
  },
}
</script>
<style lang="scss" scoped>
.box {
  width: 24px;
  height: 24px;
  background-color: white;
  position: relative;
  top: 0;
  left: 0;
  float: left;
}
</style>
