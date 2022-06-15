import route from "../../support/routes.js"
import selector from "../../support/selectors.js"

describe("View models", () => {
  beforeEach(() => {
    cy.signin()
    cy.visit(route.models)
  })

  it("should be able to view a list of models", () => {
    cy.location("pathname").should("eq", route.models)
    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(2000)
    cy.get(selector.models.item).its("length").should("gt", 0)

    cy.get(selector.models.item).each(($models) => {
      if ($models.find(selector.models.activeStatus).length > 0) {
        cy.wrap($models)
          .get(selector.models.activeStatus)
          .children()
          .eq(0)
          .should("satisfy", ($el) => {
            const classList = Array.from($el[0].classList)
            return (
              classList.includes("success--text") ||
              classList.includes("primary--text")
            ) // passes
          })
      }
    })
  })

  it("should be able to request a model", () => {
    cy.location("pathname").should("eq", route.models)
    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(2000)
    cy.get(selector.models.item).its("length").should("gt", 0)

    cy.get(selector.models.item).each(() => {
      // request a model
      cy.get(selector.models.addModel).click()
      cy.get(selector.models.requestModels).each(($el) => {
        if (!$el.attr("class").includes("v-card--disabled")) {
          cy.wrap($el).click()
          return false
        }
      })
      cy.get("button").contains("Cancel")
      cy.get("button").contains("Request 1 model").click()
      cy.location("pathname").should("eq", route.models)

      // eslint-disable-next-line cypress/no-unnecessary-waiting
      cy.wait(4000)

      // cy.get(selector.models.item)
      //   .its("length")
      //   .should("eq", $models.length + 1)

      cy.get(selector.models.pendingStatus)
        .eq(0)
        .siblings(".mdi-dots-vertical")
        .click()
      cy.get(selector.models.removeModel).eq(0).click()
      cy.get(selector.models.removeModelConfirmation)
        .get("button")
        .contains("Nevermind")
      cy.get(selector.models.removeModelConfirmation)
        .get("button")
        .contains("Yes, remove it")
        .click()

      cy.get(selector.engagement.exitDrawer).click()

      return false
    })
  })

  it("should be able to go to dashboard", () => {
    cy.location("pathname").should("eq", route.models)
    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(2000)
    cy.get(selector.models.item).its("length").should("gt", 0)

    cy.get(selector.models.item).each(($models) => {
      if ($models.find(selector.models.activeStatus).length > 0) {
        cy.wrap($models).eq(0).click()
        return false
      }
    })

    cy.location("pathname").should("eq", route.models)
  })
})
