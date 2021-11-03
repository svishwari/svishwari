import route from "../../support/routes"
import selector from "../../support/selectors"

describe("Orchestration > Audiences > Audience dashboard", () => {
  beforeEach(() => {
    cy.signin()
    cy.visit(route.audiences)
  })

  it("should be able to view Audiences List and Dashboard", () => {
    cy.location("pathname").should("eq", route.audiences)
    cy.get(selector.audience.audiencelist).its("length").should("be.gt", 0)
    cy.get(selector.audience.audiencenameclick)
      .eq(0)
      .find("a")
      .should("have.attr", "href")
      .then((href) => {
        cy.visit(href)
      })

    // should be able to validate Audiences History
    cy.get(selector.audience.audiencehistory)
      .its("length")
      .as("overviewListCount")

    cy.get("@overviewListCount").then(() => {
      cy.get(selector.audience.audiencehistory).its("length").should("be.gt", 0)
    })

    // TODO in HUS-1373 - skipped as audience (6177feb7b49e4773d5f67379) does not have engagements

    // should be able to validate engagements and delivery
    cy.get(selector.audience.engagementdelivery)
      .its("length")
      .as("overviewListCount")

    cy.get("@overviewListCount").then(() => {
      cy.get(selector.audience.engagementdelivery)
        .its("length")
        .should("be.gt", 0)
    })

    // should be able to validate Audiences Overview
    cy.get(selector.audience.overview).its("length").as("overviewListCount")

    cy.get("@overviewListCount").then(() => {
      cy.get(selector.audience.overview).its("length").should("be.gt", 0)
    })

    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(5000)

    // should be able to view Map chart
    // validate top location & income chart
    cy.get(selector.audience.mapchart).should("exist")

    // should be able to hover over bar of map chart
    // mouse hover on income chart
    cy.get(".geochart")
      .first()
      .trigger("mouseover", { eventConstructor: "MouseEvent" })

    // map state list should have 1 or more states
    // validate no of state in list
    cy.get(selector.audience.mapStateList).its("length").should("be.gt", 0)

    // should be able to view top location & income chart
    // validate top location & income chart
    cy.get(selector.audience.incomeChart).should("exist")

    // should be able to hover over bar of top location & income chart
    // mouse hover on income chart
    cy.get(".bar")
      .first()
      .trigger("mouseover", { eventConstructor: "MouseEvent" })

    // should be able to view Gender / monthly spending chart
    //validate Gender / monthly spending chart
    cy.get(selector.audience.genderSpendChart).should("exist")

    // should be able to hover over bar of Gender / monthly spending chart
    // mouse hover on income chart
    cy.get(".dot")
      .last()
      .trigger("mouseover", { eventConstructor: "MouseEvent" })

    // should be able to view Gender chart
    //validate Gender chart
    cy.get(selector.audience.genderChart).should("exist")

    // should be able to hover over arc of gender chart
    // mouse hover on income chart
    cy.get(".arc")
      .last()
      .trigger("mouseover", { force: true, eventConstructor: "MouseEvent" })

    // TODO in HUS-1373 - skipped as audience (6177feb7b49e4773d5f67379) does not have delivery history

    // should be able to open and validate delivery history
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
