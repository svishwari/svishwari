import route from "../../support/routes.js"
import selector from "../../support/selectors.js"

describe("Tests Audience", () => {
  before(() => {
    cy.signin({
      email: Cypress.env("USER_EMAIL"),
      password: Cypress.env("USER_PASSWORD"),
    })
  })

  it("should be able to view Audiences List", () => {
    //after login land in overview page
    cy.location("pathname").should("eq", route.overview)

    //click on Audience on side nav bar
    cy.get(selector.audiences).click()
    cy.location("pathname").should("eq", route.audiences)
    cy.wait(1000)
    cy.get(selector.audiences.audienceList).should(($menulist) => {
        console.log("list", $menulist)
        // expect($menulist).to.have.length("gt", 0)
      })

    // console.log("hiiiii",cy.get(selector.))
    
  })

  it("should be able to view Audiences Dashboard", () => {
    // cy.get(selector.audiences.audienceList).should(($overview) => {
    //    if(cy.get(selector.audiences.audienceList).its("length").should("gt", 0)) {
    //         console.log("hiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii")
    //    }
    // })
  })
})
