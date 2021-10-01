import route from "../../support/routes.js"
import selector from "../../support/selectors.js"

describe("Data management > Customer Profiles > Customer Profiles Dashboard", () => {
  before(() => {
    cy.signin({
      email: Cypress.env("USER_EMAIL"),
      password: Cypress.env("USER_PASSWORD"),
    })
  })

  it("should be able to navigate to customer profiles", () => {
    //click on customer profiles on side nav bar
    cy.get(selector.customerProfile.customers).click()
    cy.location("pathname").should("eq", route.customerProfiles)
  })

  it("should be able to open drawer & navigate to profile dashboard", () => {
    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(5000)
    //click on view all customer profiles button
    cy.get("button").contains("View all customers").click()
    // TODO: improve waiting for the customer list to load
    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(2000)
    cy.get(selector.customerProfile.customerID).first().click()

    // TODO: remove the need to re-login
    cy.get(selector.login.email).type(Cypress.env("USER_EMAIL"), { log: false })
    cy.get(selector.login.password).type(Cypress.env("USER_PASSWORD"), {
      log: false,
    })

    // submit the form & it will redirect to customer profile dashboard
    cy.get(selector.login.submit).click()
    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(5000)
  })

  // Inside customer profile dashboard
  it("should validate customer length card", () => {
    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(5000)
    cy.get(selector.customerProfile.customerlength).should("exist")
  })
  it("should have (Match Confidence, Life-Time Value, Conversion Time card)", () => {
    cy.get(selector.customerProfile.matchConfidence).should("exist")
    cy.get(selector.customerProfile.lifeTimeValue).should("exist")
    cy.get(selector.customerProfile.conversionTime).should("exist")
  })
  it("should have (Churn score, Last click, Last purchase date) card", () => {
    cy.get(selector.customerProfile.churnScore).should("exist")
    cy.get(selector.customerProfile.lastClick).should("exist")
    cy.get(selector.customerProfile.lastPurchaseDate).should("exist")
  })
  it("should have (Last open, Customer Insights date) card", () => {
    cy.get(selector.customerProfile.lastOpen).should("exist")
    cy.get(selector.customerProfile.customerInsights).should("exist")
  })
  it("should ++REDACTED++ value in customer insights table", () => {
    cy.get("table").contains("td", "++REDACTED++")
  })
  it("should validate contact preferencecs card", () => {
    cy.get(selector.customerProfile.contactPreferencecs).should("exist")
  })
  it("should have a customer's contact preferences (Email, Push, SMS, In-App)", () => {
    cy.get("table").contains("td", "Email")
    cy.get("table").contains("td", "Push")
    cy.get("table").contains("td", "SMS")
    cy.get("table").contains("td", "In-App")
  })
  it("should validate chord card", () => {
    cy.get(selector.customerProfile.chord).should("exist")
  })
})