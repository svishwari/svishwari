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
    cy.wait(5000)
    //click on view all customer profiles button
    cy.get("button").contains("View all customers").click()
    // TODO: improve waiting for the customer list to load
    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(2000)
    cy.get(selector.customerProfile.customerID).first().click()

    cy.get(selector.login.email).type(Cypress.env("USER_EMAIL"), { log: false })
    cy.get(selector.login.password).type(Cypress.env("USER_PASSWORD"), { log: false })

    // submit the form & it will redirect to customer profile dashboard
    cy.get(selector.login.submit).click()

    cy.wait(5000)
  })

  // Inside customer profile dashboard
  it("should validate customer length card", () => {
    cy.wait(5000)
    cy.get(selector.customerProfile.customerlength).should('exist')
  })
  it("should validate match Confidence card", () => {
    cy.get(selector.customerProfile.matchConfidence).should('exist')
  })
  it("should validate life-Time Value card", () => {
    cy.get(selector.customerProfile.lifeTimeValue).should('exist')
  })
  it("should validate conversion Time card", () => {
    cy.get(selector.customerProfile.conversionTime).should('exist')
  })
  it("should validate churn score card", () => {
    cy.get(selector.customerProfile.churnScore).should('exist')
  })
  it("should validate last click card", () => {
    cy.get(selector.customerProfile.lastClick).should('exist')
  })
  it("should validate last purchase date card", () => {
    cy.get(selector.customerProfile.lastPurchaseDate).should('exist')
  })
  it("should validate last open card", () => {
    cy.get(selector.customerProfile.lastOpen).should('exist')
  })
  it("should validate customer Insights card", () => {
    cy.get(selector.customerProfile.customerInsights).should('exist')
  })
  it("should ++REDACTED++ value in customer insights table", () => {
    cy.get('table').contains('td', '++REDACTED++');
  })
  it("should validate contact preferencecs card", () => {
    cy.get(selector.customerProfile.contactPreferencecs).should('exist')
  })
  it("should have Email in contact preferencecs table", () => {
    cy.get('table').contains('td', 'Email');
  })
  it("should have Push in contact preferencecs table", () => {
    cy.get('table').contains('td', 'Push');
  })
  it("should have SMS in contact preferencecs table", () => {
    cy.get('table').contains('td', 'SMS');
  })
  it("should validate chord card", () => {
    cy.get(selector.customerProfile.chord).should('exist')
  })
  
})
