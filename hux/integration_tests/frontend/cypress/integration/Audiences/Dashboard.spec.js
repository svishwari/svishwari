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
    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(3000)

    // Click on delivery history link if possible and open drawer
    cy.get(selector.audience.deliveryhistory).click({ force: true })

    // should be able to validate Audiences Overview
    cy.get(selector.audience.overview).its("length").as("overviewListCount")

    cy.get("@overviewListCount").then(() => {
      cy.get(selector.audience.overview).its("length").should("be.gt", 0)
    })

    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(5000)

    // verify items in delivery tab
    cy.get(selector.audience.engagementDeliveryDetails).should("exist")
    cy.get(selector.audience.standaloneDelivery).should("exist")
    cy.get(selector.audience.matchRateTable).should("exist")
    cy.get(selector.audience.lookalikes).should("exist")

    //verify items in insights tab
    cy.get(selector.audience.insightsTab).click()
    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(3000)

    // should be able to view Audience chart
    cy.get(selector.audience.audienceChart).should("exist")
    cy.get(".active-bar")
      .first()
      .trigger("mouseover", { eventConstructor: "MouseEvent" })

    // should be able to view Spend chart
    cy.get(selector.audience.spendChart).should("exist")

    // should be able to view Map chart
    cy.get(selector.audience.mapchart).should("exist")
    // should be able to hover over bar of map chart
    cy.get(".geochart")
      .first()
      .trigger("mouseover", { eventConstructor: "MouseEvent" })

    // map state list should have 1 or more states
    // validate no of state in list
    cy.get(selector.audience.mapStateList).its("length").should("be.gt", 0)
  })
})
