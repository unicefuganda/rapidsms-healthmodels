Feature: Reversion

  Scenario: Changes to HealthFacility should be logged
    Given I am logged in as admin
    And I edit a HealthFacility
    Then I should see my changes are logged