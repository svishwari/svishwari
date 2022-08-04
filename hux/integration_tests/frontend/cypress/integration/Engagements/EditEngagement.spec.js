import route from "../../support/routes.js"
import selector from "../../support/selectors.js"

describe("Orchestration > Engagement > Edit Engagement", () => {
  beforeEach(() => {
    cy.signin()
    cy.visit(route.engagements)
    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(3000)
  })

  it("should be able to modify an existing engagement description", () => {
    cy.location("pathname").should("eq", route.engagements)

    cy.get(".menu-cell-wrapper")
      .eq(0)
      .find(".mdi-dots-vertical")
      .invoke("attr", "aria-expanded", "true")
      .click({ force: true })

    cy.contains("Edit engagement").click()
    cy.contains("Yes, edit").click()
    //eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(3000)

    cy.location().should((loc) => {
      expect(loc.pathname.toString()).to.contain("/update")
    })

    // Edit engagement description
    cy.get(selector.engagement.enagagementDescription)
      .eq(0)
      .type("E2E test edited engagement")

    cy.contains("Update").click()
    cy.contains("Yes, edit")
  })

  it("should be able to modify an existing engagement name", () => {
    cy.location("pathname").should("eq", route.engagements)
    cy.get(".menu-cell-wrapper")
      .eq(0)
      .find(".mdi-dots-vertical")
      .invoke("attr", "aria-expanded", "true")
      .click({ force: true })
    cy.contains("Edit engagement").click()
    cy.contains("Yes, edit").click()
    //eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(3000)
    cy.location().should((loc) => {
      expect(loc.pathname.toString()).to.contain("/update")
    })
    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(4000)
    // Edit engagement name
    cy.get(selector.engagement.enagagementName)
      .eq(0)
      .type(" E2E test edited engagement name")
    cy.contains("Update").click()
    cy.contains("Yes, edit")
    cy.contains("E2E test edited engagement name")
  })

  it("should be able to add a destination to an audience when editing", () => {
    cy.location("pathname").should("eq", route.engagements)
    cy.get(".menu-cell-wrapper")
      .eq(0)
      .find(".mdi-dots-vertical")
      .invoke("attr", "aria-expanded", "true")
      .click({ force: true })
    cy.contains("Edit engagement").click()
    cy.contains("Yes, edit").click()
    //eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(3000)
    cy.location().should((loc) => {
      expect(loc.pathname.toString()).to.contain("/update")
    })

    // Add destination
    cy.get(selector.engagement.addDestination).first().click()
    cy.get(selector.engagement.selectDestination).first().click()
    cy.contains("Added")
  })

  it("should be able to delete an audience from an engagement", () => {
    cy.location("pathname").should("eq", route.engagements)
    cy.get(".menu-cell-wrapper")
      .eq(0)
      .find(".mdi-dots-vertical")
      .invoke("attr", "aria-expanded", "true")
      .click({ force: true })
    cy.contains("Edit engagement").click()
    cy.contains("Yes, edit").click()
    //eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(3000)
    cy.location().should((loc) => {
      expect(loc.pathname.toString()).to.contain("/update")
    })

    // Add a random audience to delete
    cy.get(selector.engagement.addAudience).click()
    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(2000)
    cy.get(selector.engagement.selectAudience).first().click()
    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(1000)
    cy.contains("Hux by Deloitte Digital").click()
    cy.get(selector.engagement.deleteAudience).last().click()
    cy.contains("Update").click()
    cy.contains("Yes, edit")
  })
})
