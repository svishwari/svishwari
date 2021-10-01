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
        // eslint-disable-next-line cypress/no-unnecessary-waiting
        cy.wait(2000)

    })

    it("should be able to validate audience list", () => {
        cy.get(selector.audience.audiencelist).its("length").should("be.gt", 0)
        
           // cy.get(selector.audience.audiencenameclick).contains("a").first().click()
    })

    it("should be able to view Audiences Dashboard", () => {
        cy.get("a[href='/audiences/13/insight']").click()
    // TODO: remove the need to re-login
     cy.get(selector.login.email).type(Cypress.env("USER_EMAIL"), { log: false })
     cy.get(selector.login.password).type(Cypress.env("USER_PASSWORD"), {
       log: false,
     })
     // submit the form & it will redirect to customer profile dashboard
     cy.get(selector.login.submit).click()
    })

    
 
})
