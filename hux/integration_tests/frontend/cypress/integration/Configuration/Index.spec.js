import route from "../../support/routes.js"
import selector from "../../support/selectors.js"

describe("View configuration", () => {
  beforeEach(() => {
    cy.signin()
    cy.visit(route.configuration)
  })

  it("should be able to view configuration screen", () => {
    cy.location("pathname").should("eq", route.configuration)
    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(2000)
    // should click on team-members tab
    cy.get(selector.configuration.teamMembers).first().click()

    // should verify the columns of the audiences table
    const tableHeaders = ["", "Name", "Email", "Access Level", "PII Access"]

    cy.get(selector.configuration.list.teamMembersTable)
      .find(selector.configuration.list.teamMembersTableHeaders)
      .children()
      .each(($elm, i) => {
        expect($elm.text()).equal(tableHeaders[i])
      })

    cy.get(selector.configuration.teamMemberDrawer.teamMemberRequest).click()
    cy.get(selector.configuration.teamMemberDrawer.firstName)
      .eq(0)
      .type("Sarah")
    cy.get(selector.configuration.teamMemberDrawer.lastName)
      .eq(0)
      .type("Huxley")
    cy.get(selector.configuration.teamMemberDrawer.email)
      .eq(0)
      .type("Huxley@gmail.com")
    cy.get(selector.configuration.teamMemberDrawer.accessLevel).click()
    cy.get(".dropdown-menuitems").contains("Admin").click()
    cy.get(selector.configuration.teamMemberDrawer.togglePii).click()
    cy.get(selector.configuration.teamMemberDrawer.requestText)
      .eq(0)
      .type("New team member")
    // should click on requestbutton
    cy.get(selector.configuration.teamMemberDrawer.request).click()
    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(1000)
    cy.get(selector.configuration.teamMemberDrawer.teamMemberRequest).click()
    cy.get(selector.configuration.teamMemberDrawer.closeDrawer).click()
    // should click on module-solutions tab
    cy.get(selector.configuration.moduleSolution).click()
    // should click & checked on checkbox to show only active items
    cy.get(selector.configuration.activeItem).click({ force: true })
    // should click & un-checked on checkbox to show all items
    cy.get(selector.configuration.activeItem).click({ force: true })
    // should open tips menu
    cy.get(selector.configuration.tipsMenu).click()
    // should close tips menu
    cy.get(selector.configuration.tipsMenu).click()
  })
})
