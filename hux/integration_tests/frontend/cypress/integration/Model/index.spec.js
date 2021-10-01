import route from "../../support/routes.js"
import selector from "../../support/selectors.js"

describe("Decisioning > models", () => {
    before(() => {
        cy.signin({
            email: Cypress.env("USER_EMAIL"),
            password: Cypress.env("USER_PASSWORD"),
        })
    })

    it("should be able to view a list of models", () => {
        cy.get(selector.nav.models).click()

        cy.location("pathname").should("eq", route.models)

        cy.get(selector.models.item).should(($models) => {
            expect($models).to.have.length(2)

            // propensity to unsubscribe model
            expect($models.eq(0).find(selector.card.title)).to.contain(
                "Propensity to Unsubscribe",
            )
            expect($models.eq(0).find(selector.card.description)).to.contain(
                "Propensity of a customer unsubscribing to emails.",
            )

            // LTV model
            expect($models.eq(1).find(selector.card.title)).to.contain("LTV")
            expect($models.eq(1).find(selector.card.description)).to.contain(
                "Propensity of a customer unsubscribing to emails.",
            )
        })

        cy.get(selector.models.item).first().click()
    })

    it("view and validate overview", () => {
        //validate performance metric exist by getting total no. of them
        cy.get(selector.models.performancemetric)
  .then(dataId => console.log('dataId : ', dataId.length));

        cy.get(selector.models.performancemetric)
            .its("length")
            .as("overviewListCount")
        cy.get("@overviewListCount").then(() => {
            cy.get(selector.models.performancemetric).its("length").should("eq", 5)
        })

        cy.get(selector.models.performancemetric).should(($models) => {
          
           let value = $models.text()
           let data = value.replace(" ", ",");
           console.log("data++++++++++++++++++++++++++++++++++++", data)
        })
    })

    it("should be able to view and validate Drift and Feature chart", () => {
        //validate Gender chart
        cy.get(selector.models.driftchart).its("length").should("be.gt", 0)
        cy.get(selector.models.featurechart).its("length").should("be.gt", 0)
        // scroll down
        cy.scrollTo("bottom", { duration: 1000 })
    })

    it("validate feature and lift table", () => {
        cy.get(selector.models.lifttable).its("length").should("be.gt", 0)
        cy.get(selector.models.featuretable).its("length").should("be.gt", 0)
        // eslint-disable-next-line cypress/no-unnecessary-waiting
        cy.wait(1000)
    })

    it("should be able to view version history list", () => {
        //open version history drawer
        cy.get(selector.models.versionhistorybutton).click()

        //validate the history list
        cy.get(selector.models.versionhistory).its("length").should("gt", 0)


    })

})
