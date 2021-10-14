import route from "../../support/routes.js"
import selector from "../../support/selectors.js"

describe("audience dashboard test suite", () => {
  before(() => {
    cy.signin({
      email: Cypress.env("USER_EMAIL"),
      password: Cypress.env("USER_PASSWORD"),
    })
  })

  it("should be able to view Audiences List and Dashboard", () => {
    // after login land in the overview page
    cy.location("pathname").should("eq", route.overview)

    //click on engagement on side nav bar and route in engagement screen
    cy.get(selector.audiences).click()
    cy.location("pathname").should("eq", route.audiences)
    cy.get(selector.audience.audiencelist).its("length").should("be.gt", 0)
    cy.get(selector.audience.audiencenameclick)
      .eq(2)
      .find("a")
      .should("have.attr", "href")
      .then((href) => {
        cy.visit(href)
      })
  })

  it("should be able to validate Audiences History", () => {
    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(5000)
    cy.get(selector.audience.audiencehistory)
      .its("length")
      .as("overviewListCount")

    cy.get("@overviewListCount").then(() => {
      cy.get(selector.audience.audiencehistory).its("length").should("be.gt", 0)
    })
  })

  it("should be able to validate engagements and delivery", () => {
    cy.get(selector.audience.engagementdelivery)
      .its("length")
      .as("overviewListCount")

    cy.get("@overviewListCount").then(() => {
      cy.get(selector.audience.engagementdelivery)
        .its("length")
        .should("be.gt", 0)
    })
  })

  it("should be able to validate Audiences Overview", () => {
    cy.get(selector.audience.overview).its("length").as("overviewListCount")

    cy.get("@overviewListCount").then(() => {
      cy.get(selector.audience.overview).its("length").should("be.gt", 0)
    })
  })

  // TODO: temporarily skipping - HUS-1267
  it("should be able to view Map chart", () => {
    // validate top location & income chart
    cy.get(selector.audience.mapchart).should("exist")
  })

  // TODO: temporarily skipping - HUS-1267
  it("should be able to hover over bar of map chart", () => {
    // mouse hover on income chart
    cy.get(".geochart")
      .first()
      .trigger("mouseover", { eventConstructor: "MouseEvent" })
  })

  // TODO: temporarily skipping - HUS-1267
  it("map state list should have 52 state", () => {
    // validate no of state in list
    cy.get(selector.audience.mapStateList).its("length").should("eq", 51)
  })

  // TODO: temporarily skipping - HUS-1267
  it("should be able to view top location & income chart", () => {
    // validate top location & income chart
    cy.get(selector.audience.incomeChart).should("exist")
  })

  // TODO: temporarily skipping - HUS-1267
  it("should be able to hover over bar of top location & income chart", () => {
    // mouse hover on income chart
    cy.get(".bar")
      .first()
      .trigger("mouseover", { eventConstructor: "MouseEvent" })
  })

  // TODO: temporarily skipping - HUS-1267
  it("should be able to view Gender / monthly spending chart", () => {
    //validate Gender / monthly spending chart
    cy.get(selector.audience.genderSpendChart).should("exist")
  })

  // TODO: temporarily skipping - HUS-1267
  it("should be able to hover over bar of Gender / monthly spending chart", () => {
    // mouse hover on income chart
    cy.get(".chart-section > svg")
      .eq(1)
      .trigger("mouseover", { eventConstructor: "MouseEvent" })
  })

  // TODO: temporarily skipping - HUS-1267
  it("should be able to view Gender chart", () => {
    //validate Gender chart
    cy.get(selector.audience.genderChart).should("exist")
  })

  // TODO: temporarily skipping - HUS-1267
  it("should be able to hover over arc of gender chart", () => {
    // mouse hover on income chart
    cy.get(".arc")
      .first()
      .trigger("mouseover", { force: true, eventConstructor: "MouseEvent" })
  })

  // TODO: temporarily skipping - HUS-1267
  it("should be able to open and validate deliver history", () => {
    cy.get(selector.audience.deliveryhistory).click()

    cy.get(selector.audience.deliveryhistorydrawer)
      .its("length")
      .as("deliveryhistory")

    cy.get("@deliveryhistory").then(() => {
      cy.get(selector.audience.deliveryhistorydrawer)
        .its("length")
        .should("be.gt", 0)
    })
  })
})
