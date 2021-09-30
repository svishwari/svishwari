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
        cy.wait(2000)
    })

    it("should be able to view Audiences Dashboard", () => {
        cy.get(selector.audience.audiencelist).its("length").should("be.gt", 0)
    })
})
