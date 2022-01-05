import route from "../../support/routes"
import selector from "../../support/selectors"
import { randomName } from "../../support/utils"

let randomAudienceName = randomName()

describe("Customer Insights > Segment Playground", () => {
  beforeEach(() => {
    cy.signin()
    cy.visit(route.segmentPlayground)
    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(3000)
  })

  it("should be able to save segment as a new audience", () => {
    cy.location("pathname").should("eq", route.segmentPlayground)
    cy.get(selector.segmentPlayground.addNewAttr).click()
    // Select attribute
    cy.get(selector.segmentPlayground.selectAttrBtn).click()
    cy.get("div[class='dropdown-menuitems']").contains("Email").click()

    // Select operator
    cy.get(selector.segmentPlayground.selectOperatorBtn).click()
    cy.get("div[class='dropdown-menuitems']")
      .contains("Equals")
      .click({ force: true })

    // Select Value
    cy.get(selector.segmentPlayground.autoCompleteBtn).click()
    cy.get(".v-autocomplete__content").contains(".com").click({ force: true })

    // Wait for api call to complete
    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(3000)

    // click on Save as an audience
    cy.get(selector.audience.actionAudience).click()

    // should fill new audience name and description
    // add new audience name
    cy.get(selector.audience.audienceName)
      .eq(0)
      .type(`E2E test audience ${randomAudienceName}`)

    // Click on save audience icon
    cy.get(".confirm-modal-wrapper")
      .find("button")
      .contains("Save")
      .click({ force: true })

    // Wait for audience to be created
    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(3000)
  })

  // This test case is written to delete an audience created above
  it("should be able to delete a newly added audience", () => {
    cy.visit(route.audiences)
    //eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(2000)

    cy.get(".menu-cell-wrapper").each(($el) => {
      if ($el.text().includes(`E2E test audience ${randomAudienceName}`)) {
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
