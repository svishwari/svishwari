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

    // click on customer list tab
    cy.get(selector.customerProfile.customerListTab).click()

    // select first customer in list
    cy.get(selector.customerProfile.customerID).first().click()

    // TODO: remove the need to re-login
    // cy.reLogin()

    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(5000)

    // should validate customer length card
    cy.get(selector.customerProfile.customerlength).should("exist")

    // should have (Match Confidence, Conversion Time card, Last click, Last purchase date)
    cy.get(selector.customerProfile.matchConfidence).should("exist")
    cy.get(selector.customerProfile.conversionTime).should("exist")
    cy.get(selector.customerProfile.lastClick).should("exist")
    cy.get(selector.customerProfile.lastPurchaseDate).should("exist")

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

    //should validate customer events drawer
    cy.get(selector.customerProfile.eventsDrawerButton).click()
    cy.get(selector.customerProfile.customerEventRow).should("exist")
  })
})
