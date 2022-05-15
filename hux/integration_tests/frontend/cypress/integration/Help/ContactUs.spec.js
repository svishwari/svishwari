import route from "../../support/routes.js"
import selector from "../../support/selectors.js"

describe("Contact Us", () => {
  beforeEach(() => {
    cy.signin()
    cy.visit(route.home)
  })

  it("should be able to explore contact us in help", () => {
    cy.get(selector.topNav.help).click()
    cy.get(selector.topNav.contactus).click()
    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(1000)
    cy.get(selector.contactUS.contactUsOptions).should(($options) => {
      expect($options).to.have.length(3)
      expect($options.eq(0)).to.contain("General feedback")
      expect($options.eq(1)).to.contain("Report a bug")
      expect($options.eq(2)).to.contain("Email us")
    })
    cy.get(selector.contactUS.contactUsOptions).eq(1).click()
    cy.get(selector.contactUS.reportBugSubject).eq(0).type("Bug subject")
    cy.get(selector.contactUS.reportBugDescription)
      .eq(0)
      .type("Bug description")
    cy.get("button").contains("Back").eq(0).click()
    cy.get("button").contains("Cancel").eq(0).click()
  })
})
