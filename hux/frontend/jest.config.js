process.env.TZ = "Pacific/Honolulu"

module.exports = {
  preset: "@vue/cli-plugin-unit-jest",
  setupFilesAfterEnv: ["./jest.setupTests.js"],
}
