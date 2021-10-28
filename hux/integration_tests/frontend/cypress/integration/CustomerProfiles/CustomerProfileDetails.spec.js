import route from "../../support/routes"
import selector from "../../support/selectors"

describe("Data management > Customer Profiles > Customer Profiles Dashboard", () => {
  beforeEach(() => {
    cy.signin()
    cy.visit(route.customerProfiles)
  })

  it("should be able to navigate to customer profiles", () => {
    cy.location("pathname").should("eq", route.customerProfiles)

    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(5000)

    // click on view all customer profiles button
    cy.get(selector.customerProfile.customeroverview).eq(0).click()

    // select first customer in drawer
    cy.get(selector.customerProfile.customerID).first().click()

    // TODO: remove the need to re-login
    // cy.reLogin()

    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(5000)

    // should validate customer length card
    cy.get(selector.customerProfile.customerlength).should("exist")

    // should have (Match Confidence, Life-Time Value, Conversion Time card)
    cy.get(selector.customerProfile.matchConfidence).should("exist")
    cy.get(selector.customerProfile.lifeTimeValue).should("exist")
    cy.get(selector.customerProfile.conversionTime).should("exist")

    // should have (Churn score, Last click, Last purchase date) card
    cy.get(selector.customerProfile.churnScore).should("exist")
    cy.get(selector.customerProfile.lastClick).should("exist")
    cy.get(selector.customerProfile.lastPurchaseDate).should("exist")

    // should have (Last open, Customer Insights date) card
    cy.get(selector.customerProfile.lastOpen).should("exist")
    cy.get(selector.customerProfile.customerInsights).should("exist")

    // should ++REDACTED++ value in customer insights table
    cy.get("table").contains("td", "++REDACTED++")

    // should validate contact preferencecs card
    cy.get(selector.customerProfile.contactPreferencecs).should("exist")

    // should have a customer's contact preferences (Email, Push, SMS, In-App)
    cy.get("table").contains("td", "Email")
    cy.get("table").contains("td", "Push")
    cy.get("table").contains("td", "SMS")
    cy.get("table").contains("td", "In-App")

    // should validate chord card
    cy.get(selector.customerProfile.chord).should("exist")
  })
})
