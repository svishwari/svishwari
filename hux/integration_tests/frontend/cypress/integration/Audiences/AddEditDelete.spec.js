import route from "../../support/routes"
import selector from "../../support/selectors"
import { randomName } from "../../support/utils"

let audienceName = randomName()

describe("Orchestration > Audience > Add, Edit and Delete Audience", () => {
  beforeEach(() => {
    cy.signin()
    cy.visit(route.audiences)
    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(3000)
  })

  // For adding a new audience
  it("should be able to add/configure a new audience via Segment Playground", () => {
    cy.location("pathname").should("eq", route.audiences)

    cy.get(selector.audience.addNewAudience).click()
    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(2000)

    cy.location("pathname").should("eq", route.segmentPlayground)
    cy.get(selector.segmentPlayground.addNewAttr).click()

    // Attribute selection
    cy.get(selector.segmentPlayground.selectAttrBtn).click()
    cy.get("div[class='dropdown-menuitems']").contains("Email").click()

    // Operator selection
    cy.get(selector.segmentPlayground.selectOperatorBtn).click()
    cy.get("div[class='dropdown-menuitems']")
      .contains("Equals")
      .click({ force: true })

    // Value selection
    cy.get(selector.segmentPlayground.autoCompleteBtn).click()
    cy.get(".v-autocomplete__content").contains(".com").click({ force: true })

    // Waiting for fetch the response
    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(2000)

    // click on Save as an audience
    cy.get(selector.audience.actionAudience).click()

    // should fill new audience name and description
    // add new audience name
    cy.get(selector.audience.audienceName)
      .eq(0)
      .type(`Test audience ${audienceName}`)

    // Click on save audience icon
    cy.get(".confirm-modal-wrapper")
      .find("button")
      .contains("Save")
      .click({ force: true })

    // Wait for audience to be created
    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(2000)
  })

  // TODO: In local env. the create, edit and delete are not being able to perform one after another in a single it()
  // due to cypress unable to find the 'delete audience' option, because of its parent element having 'display: none' set.

  // For editing the above added audience
  it("should be able to edit a newly added audience via Segment Playground", () => {
    cy.location("pathname").should("eq", route.audiences)
    cy.get(".menu-cell-wrapper").each(($el) => {
      if ($el.text().includes(`Test audience ${audienceName}`)) {
        // Make the vertical dots visible
        cy.wrap($el)
          .find(".mdi-dots-vertical")
          .invoke("attr", "aria-expanded", "true")
          .click({ force: true })

        cy.contains("Edit audience").click()
        cy.contains("Yes, edit").click()
        //eslint-disable-next-line cypress/no-unnecessary-waiting
        cy.wait(5000)

        cy.location().should((loc) => {
          expect(loc.pathname.toString()).to.contain("/update")
        })

        // Edit audience name
        cy.get(selector.audience.editAudienceName).eq(0).type(` edited`)

        // Waiting for fetch the response
        // eslint-disable-next-line cypress/no-unnecessary-waiting
        cy.wait(2000)

        // click on Apply changes and Save
        cy.get(selector.audience.actionAudience).click()

        // Wait for audience to be edited
        // eslint-disable-next-line cypress/no-unnecessary-waiting
        cy.wait(2000)
      }
    })
  })

  // For deleting the above added audience
  it("should be able to delete a newly added audience", () => {
    cy.location("pathname").should("eq", route.audiences)
    cy.get(".menu-cell-wrapper").each(($el) => {
      if ($el.text().includes(`Test audience ${audienceName} edited`)) {
        // Make the vertical dots visible
        cy.wrap($el)
          .find(".mdi-dots-vertical")
          .invoke("attr", "aria-expanded", "true")
          .click({ force: true })

        cy.contains("Delete audience").click()
        cy.contains("Yes, delete it").click()
        //eslint-disable-next-line cypress/no-unnecessary-waiting
        cy.wait(2000)
      }
    })
  })
})
