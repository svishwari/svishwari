import route from "../../support/routes"
import selector from "../../support/selectors"

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
    cy.get(selector.audience.audienceName).eq(0).type(`E2E test audience`)

    // Click on save audience icon
    cy.get(".confirm-modal-wrapper")
      .find("button")
      .contains("Save")
      .click({ force: true })

    // Wait for audience to be created
    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(2000)
  })

  // For editing the above added audience
  it("should be able to edit a newly added audience via Segment Playground", () => {
    cy.visit(route.audiences)
    //eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(2000)

    cy.get(".menu-cell-wrapper").each(($el) => {
      if ($el.text().includes(`E2E test audience`)) {
        // Make the vertical dots visible
        cy.wrap($el)
          .find(".mdi-dots-vertical")
          .invoke("attr", "aria-expanded", "true")
          .click({ force: true })

        cy.contains("Edit audience").click()
        //eslint-disable-next-line cypress/no-unnecessary-waiting
        cy.wait(4000)

        cy.location().should((loc) => {
          expect(loc.pathname.toString()).to.contain("/update")
        })

        //  cy.location("pathname").contains("update")

        // Edit audience name
        cy.get(selector.audience.editAudienceName)
          .eq(0)
          .type(`E2E test audience edited`)

        // Add a new attribute to existing audience
        // Attribute selection
        cy.get(selector.segmentPlayground.selectAttrBtn).click()
        cy.get("div[class='dropdown-menuitems']").contains("Gender").click()

        // Operator selection
        cy.get(selector.segmentPlayground.selectOperatorBtn).click()
        cy.get("div[class='dropdown-menuitems']")
          .contains("Equals")
          .click({ force: true })

        // Value selection
        cy.get(selector.segmentPlayground.autoCompleteBtn).click()
        cy.get(".v-autocomplete__content")
          .contains("Male")
          .click({ force: true })

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
    cy.visit(route.audiences)
    //eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(2000)

    cy.get(".menu-cell-wrapper").each(($el) => {
      if ($el.text().includes(`E2E test audience edited`)) {
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
