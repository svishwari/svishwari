import { listOfMonths, listOfYears } from "@/utils"

describe("Utils", () => {
  describe("List of months", () => {
    it("Should provide an array of month names", () => {
      const expected = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
      ]

      expect(listOfMonths()).toEqual(expect.arrayContaining(expected))
    })
  })

  describe("List of years", () => {
    it("Should provide an array of years", () => {
      const expected = [
        "2021",
        "2020",
        "2019",
        "2018",
        "2017",
        "2016",
        "2015",
        "2014",
        "2013",
        "2012",
      ]

      expect(listOfYears()).toEqual(expect.arrayContaining(expected))
      expect(listOfYears(3)).toEqual(
        expect.arrayContaining(expected.slice(0, 3))
      )
    })
  })
})
