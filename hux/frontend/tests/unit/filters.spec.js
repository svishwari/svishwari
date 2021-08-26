import filters from "@/filters"

describe("Filters", () => {
  describe("Date filter", () => {
    it("should display date in format as specified", () => {
      expect(filters.Date("2019-01-25","DD/MM/YYYY")).toEqual("25/01/2019")
      expect(filters.Date("2019-01-25","[YYYYescape] YYYY-MM-DDTHH:mm:ss[Z]")).toEqual("YYYYescape 2019-01-25T00:00:00Z")
      expect(filters.Date("2019-01-25","M/D/YYYY [at] h:mm A")).toEqual("1/25/2019 at 12:00 AM")
      expect(filters.Date("2019-01-25")).toEqual("1/25/2019 at 12:00 AM")
    })
  })

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
    it("should convert and display a number as a percentage", () => {
      expect(filters.Percentage(0)).toEqual("0%")
      expect(filters.Percentage(0.01)).toEqual("1%")
      expect(filters.Percentage(0.02)).toEqual("2%")
      expect(filters.Percentage(0.33)).toEqual("33%")
      expect(filters.Percentage(0.044)).toEqual("4%")
      expect(filters.Percentage(0.9949)).toEqual("99%")
      expect(filters.Percentage(1.1005)).toEqual("110%")
    })

    it("should convert and display a number as a percentage up to two decimal places", () => {
      expect(filters.Percentage(0.0000495, false)).toEqual("0%")
      expect(filters.Percentage(0.051, false)).toEqual("5.1%")
      expect(filters.Percentage(0.01249995, false)).toEqual("1.25%")
    })

    it("should not convert values that are not percentages", () => {
      const nonPercentageValues = [null, undefined, {}, true, false]
      nonPercentageValues.forEach((value) => {
        expect(filters.Percentage(value)).toEqual(value)
      })
    })
  })

  describe("Empty filter", () => {
    it("should handle empty values with a placeholder", () => {
      const placeholder = "—"
      const emptyValues = [null, undefined, "", "    "]

      emptyValues.forEach((value) => {
        expect(filters.Empty(filters.Numeric(value))).toEqual(placeholder)
        expect(filters.Empty(filters.Percentage(value))).toEqual(placeholder)
      })
    })

    it("should not convert numeric and percentage values with a placeholder", () => {
      const placeholder = "—"
      const nonEmptyValues = [0.0123, 0, 1, "0", "1", -1.23, "Hello"]

      nonEmptyValues.forEach((value) => {
        expect(filters.Empty(value)).not.toEqual(placeholder)
        expect(filters.Empty(filters.Numeric(value))).not.toEqual(placeholder)
        expect(filters.Empty(filters.Percentage(value))).not.toEqual(
          placeholder
        )
      })
    })

    it("should allow for custom placeholders as well, when provided", () => {
      expect(filters.Empty(null, "N/A")).toEqual("N/A")
    })
  })
})
