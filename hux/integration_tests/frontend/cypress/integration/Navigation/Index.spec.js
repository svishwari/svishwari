import route from "../../support/routes.js"
import selector from "../../support/selectors.js"

describe("View Navigation", () => {
    before(() => {
        cy.signin({
            email: Cypress.env("USER_EMAIL"),
            password: Cypress.env("USER_PASSWORD"),
        })
    })

    it("should be able to view navigation", () => {
        // after login land in the overview page
        cy.location("pathname").should("eq", route.overview)

        //click on engagement on side nav bar and route in engagement screen 
        cy.get(selector.engagements).click()
        cy.location("pathname").should("eq", route.engagements)
        // eslint-disable-next-line cypress/no-unnecessary-waiting
        cy.wait(1000)
        // from the header click on the help icon  
        cy.get(selector.navigation.help).click()
        // eslint-disable-next-line cypress/no-unnecessary-waiting
        cy.wait(500)
        // once menu drop down get open click on the contact us menu
        cy.get(selector.navigation.contactus).click()
        // eslint-disable-next-line cypress/no-unnecessary-waiting
        cy.wait(500)

        //click on audiences on side nav bar and route in audiences screen
        cy.get(selector.audiences).click()
        cy.location("pathname").should("eq", route.audiences)
        // eslint-disable-next-line cypress/no-unnecessary-waiting
        cy.wait(1000)

        // from the header click on the add icon  
        cy.get(selector.navigation.add).click()
        // eslint-disable-next-line cypress/no-unnecessary-waiting
        cy.wait(500)

        //click on models on side nav bar and route in models screen
        cy.get(selector.models.models).click()
        cy.location("pathname").should("eq", route.models)

        //click on identity resolution on side nav bar and route in identity resolution screen
        cy.get(selector.idr.identityResolution).click()
        cy.location("pathname").should("eq", route.identityResolution)

        //click on audiences on side nav bar and route in audiences screen
        cy.get(selector.connections).click()
        cy.location("pathname").should("eq", route.connections)
        // eslint-disable-next-line cypress/no-unnecessary-waiting
        cy.wait(1000)
        // click on the profile drop menu 
        cy.get(selector.navigation.profiledropdown).click()
        // eslint-disable-next-line cypress/no-unnecessary-waiting
        cy.wait(500)
        // select the profile option
        cy.get(selector.navigation.profile).click()
    })

})
