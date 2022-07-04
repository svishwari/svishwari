import route from "../../support/routes"
import selector from "../../support/selectors"
import { randomName } from "../../support/utils"

let engagementName = randomName()

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

    cy.get(selector.audience.engagementDeliveryDetails)
      .contains("An engagement")
      .click()

    cy.get(selector.audience.selectEngagement).its("length").should("gte", 0)
    cy.contains("Create a new engagement").click()
    cy.get(selector.audience.newEngagementFirstName)
      .eq(0)
      .type(`Test Engagement ${engagementName}`)
    cy.get(selector.audience.createNewEngagement).click()

    cy.get(selector.audience.addNewDestination).eq(0).click()
    // Select the first destination from the existing ones
    cy.get(selector.engagement.selectDestination).eq(0).click()
    cy.get(selector.engagement.exitDrawer).click()
    cy.get(selector.audience.addNewDestination).eq(0).click()

    cy.get("body").then(($body) => {
      if ($body.find(selector.engagement.salesForceAddButton).length > 0) {
        cy.get(selector.engagement.salesForceAddButton).click()
        // Add new data extension name
        cy.get(selector.engagement.dataExtensionName)
          .eq(1)
          .type(`Test Extension ${engagementName}`)
        // Close the data extension drawer
        cy.get(selector.engagement.exitDataExtensionDrawer).click()
      }
    })
    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(1000)
    // Close the add destination drawer
    cy.get(selector.engagement.exitDrawer).click()

    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(4000)

    // verify items in delivery tab
    cy.get(selector.audience.refreshAudience).click()

    cy.get(selector.audience.engagementdelivery).contains("Deliver all").click()

    cy.get(selector.audience.destinationRemove).each(($el) => {
      if ($el.text().includes("Salesforce")) {
        // Make the vertical dots visible
        cy.wrap($el)
          .find(".mdi-dots-vertical")
          .invoke("attr", "aria-expanded", "true")
          .click({ force: true })

        cy.contains("Deliver now").click()

        cy.wrap($el)
          .find(".mdi-dots-vertical")
          .invoke("attr", "aria-expanded", "true")
          .click({ force: true })

        cy.contains("Remove destination").click()
        cy.contains("Yes, remove it").click()
      }
    })

    cy.get(selector.audience.engagementdelivery)
      .eq(0)
      .find(".mdi-dots-vertical")
      .eq(0)
      .click()

    cy.contains("Remove engagement").click()
    cy.contains("Yes, remove it").click()

    cy.get(selector.audience.standaloneDelivery).should("exist")
    cy.get(selector.audience.standaloneDelivery).contains("Deliver all").click()
    cy.get(selector.audience.standaloneDestinationDrawer).click()
    // Select the first destination from the existing ones
    cy.get(selector.engagement.selectDestination)
      .contains(/\bAdd\b/g)
      .eq(0)
      .click()
    cy.get(selector.engagement.exitDrawer).click()

    cy.get(selector.audience.replaceAudience).eq(0).click()
    cy.get(selector.audience.standaloneDestinations)
      .eq(0)
      .find(".mdi-dots-vertical")
      .invoke("attr", "aria-expanded", "true")
      .click({ force: true })
    cy.contains("Deliver now").click()

    cy.get(selector.audience.standaloneDestinations)
      .eq(0)
      .find(".mdi-dots-vertical")
      .invoke("attr", "aria-expanded", "true")
      .click({ force: true })
    cy.contains("Open destination")

    cy.get(selector.audience.standaloneDestinations)
      .eq(0)
      .find(".mdi-dots-vertical")
      .invoke("attr", "aria-expanded", "true")
      .click({ force: true })
    cy.contains("Remove destination")

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

    cy.get(selector.audience.editAudience).click()
    cy.contains("Nevermind")
    cy.get(selector.audience.audienceOptions).click()
    cy.contains("Favorite")
    cy.contains("Download as")
    cy.contains("Delete audience")
  })
})
