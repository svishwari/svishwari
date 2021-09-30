import { listOfMonths, listOfYears, endOfMonth } from "@/utils"

describe("Utils", () => {
  describe("List of months", () => {
    it("Should provide an array of all the month names", () => {
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
        "December",
      ]
      const actual = listOfMonths()

      expect(actual).toEqual(expected)
    })

    it("Should provide an array of months between a start and end month", () => {
      const expected = ["March", "April", "May", "June"]
      const actual = listOfMonths({
        startMonth: "March",
        endMonth: "June",
      })

      expect(actual).toEqual(expected)
    })

    it("Should provide an array of months between a start month to the end of the year", () => {
      const expected = ["September", "October", "November", "December"]
      const actual = listOfMonths({ startMonth: "September" })

      expect(actual).toEqual(expected)
    })

    it("Should provide an array of months between the start of the year to the end month", () => {
      const expected = ["January", "February", "March", "April"]
      const actual = listOfMonths({ endMonth: "April" })

      expect(actual).toEqual(expected)
    })
  })

  describe("List of years", () => {
    it("Should provide an array of the past 5 years", () => {
      const year = new Date().getFullYear()
      const len = { length: 5 }
      const expected = Array.from(len, (_, i) => String(year - i)).reverse()
      const actual = listOfYears()

      expect(actual).toEqual(expected)
    })

    it("Should provide an array of years between a start and end year", () => {
      const expected = ["1999", "2000", "2001", "2002", "2003", "2004", "2005"]
      const actual = listOfYears({
        startYear: "1999",
        endYear: "2005",
      })

      expect(actual).toEqual(expected)
    })
  })

  describe("End of month", () => {
    it("Should provide the last date of a given month", () => {
      const expected = "2020-02-29"
      const actual = endOfMonth("2020-02-01")
      expect(actual).toEqual(expected)
    })
  })
})
