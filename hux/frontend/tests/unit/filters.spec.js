import filters from "@/filters"

describe("Filters", () => {
  describe("Numeric filter", () => {
    it("should display numbers up to two decimal places, by default", () => {
      expect(filters.Numeric(0)).toEqual("0")
      expect(filters.Numeric(16.0)).toEqual("16")
      expect(filters.Numeric(1.5)).toEqual("1.5")
      expect(filters.Numeric(210.39012509562936345674576889)).toEqual("210.39")
    })

    it("should display commas for the thousands separator", () => {
      expect(filters.Numeric(45450)).toEqual("45,450")
      expect(filters.Numeric(2000)).toEqual("2,000")
      expect(filters.Numeric(11324502100.0099, true)).toEqual("11,324,502,100")
    })

    it("should display abbreviated numbers in the thousands or millions", () => {
      expect(filters.Numeric(9502.8247, false, true)).toEqual("9.5K")
      expect(filters.Numeric(1349257.00521, false, true)).toEqual("1.35M")
    })

    it("should append the number with the provided string", () => {
      expect(
        filters.Numeric(6.137, true, false, false, false, " seconds")
      ).toEqual("6 seconds")
      expect(
        filters.Numeric(1044.8247, true, false, false, false, "x")
      ).toEqual("1,045x")
    })
  })

  describe("Percentage filter", () => {
    it("should convert and display values as a percentage", () => {
      expect(filters.Percentage(0)).toEqual("0%")
      expect(filters.Percentage(0.01)).toEqual("1%")
      expect(filters.Percentage(0.02)).toEqual("2%")
      expect(filters.Percentage(0.33)).toEqual("33%")
      expect(filters.Percentage(0.044)).toEqual("4%")
      expect(filters.Percentage(0.9949)).toEqual("99%")
      expect(filters.Percentage(1.1005)).toEqual("110%")
    })
  })
})
