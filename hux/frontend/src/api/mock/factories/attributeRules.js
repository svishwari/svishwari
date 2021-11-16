const attributeRules = {
  text_operators: {
    contains: "Contains",
    not_contains: "Does not contain",
    equals: "Equals",
    not_equals: "Does not equal",
  },
  rule_attributes: {
    model_scores: {
      propensity_to_unsubscribe: {
        name: "Propensity to unsubscribe",
        type: "range",
        min: 0,
        max: 1,
        steps: 0.05,
        values: [
          [0.024946739301654024, 11427],
          [0.07496427927927932, 11322],
          [0.12516851755300673, 11508],
          [0.17490722222222196, 11340],
          [0.22475237305041784, 11028],
          [0.27479887395267527, 10861],
          [0.32463341819221986, 10488],
          [0.3748012142488386, 9685],
          [0.424857603462838, 9472],
          [0.4748600344076149, 8719],
          [0.5247584942372063, 8069],
          [0.5748950945245762, 7141],
          [0.6248180486698927, 6616],
          [0.6742800016897607, 5918],
          [0.7240552640642912, 5226],
          [0.7748771045863732, 4666],
          [0.8245333194000475, 4067],
          [0.8741182097701148, 3480],
          [0.9238849161073824, 2980],
          [0.9741102931596075, 2456],
        ],
      },
      ltv_predicted: {
        name: "Predicted lifetime value",
        type: "range",
        min: 0,
        max: 998.8,
        steps: 20,
        values: [
          [25.01266121420892, 20466],
          [74.90030921605447, 19708],
          [124.93400516206559, 18727],
          [174.636775834374, 17618],
          [224.50257155855883, 15540],
          [274.4192853530467, 14035],
          [324.5557537562226, 11650],
          [374.0836229319332, 9608],
          [424.08129865033845, 7676],
          [474.0542931632165, 6035],
          [523.573803219089, 4610],
          [573.6697460367739, 3535],
          [623.295952316871, 2430],
          [674.0507447610822, 1737],
          [722.9281163886425, 1127],
          [773.0364963285016, 828],
          [823.8157326407769, 515],
          [872.0919142507652, 327],
          [922.9545223902437, 205],
          [975.5857619444447, 108],
        ],
      },
      propensity_to_purchase: {
        name: "Propensity to purchase",
        type: "range",
        min: 0,
        max: 1,
        steps: 0.05,
        values: [
          [0.02537854973094943, 11522],
          [0.07478697708351197, 11651],
          [0.1248279331496129, 11249],
          [0.1747714344852409, 11112],
          [0.2249300773782431, 10985],
          [0.2748524565641576, 10763],
          [0.32492868003913766, 10220],
          [0.3745931779533858, 9997],
          [0.42461185061435747, 9278],
          [0.4747488547963946, 8767],
          [0.5245381213163091, 8144],
          [0.5748252185124849, 7368],
          [0.6245615267403664, 6694],
          [0.6745955099966098, 5902],
          [0.7241630427350405, 5265],
          [0.7744812744022826, 4559],
          [0.824692568267536, 3977],
          [0.8744300917431203, 3379],
          [0.9241139159001297, 3044],
          [0.9740590406189552, 2585],
        ],
      },
    },
    general: {
      age: {
        name: "Age",
        type: "range",
        min: 18,
        max: 79,
      },
      email: {
        name: "Email",
        type: "list",
        options: [
          {
            "fake.com": "fake.com",
          },
        ],
      },
      gender: {
        name: "Gender",
        type: "list",
        options: [
          {
            female: "Female",
          },
          {
            male: "Male",
          },
          {
            other: "Other",
          },
        ],
      },
      location: {
        name: "Location",
        country: {
          name: "Country",
          type: "list",
          options: [
            {
              US: "USA",
            },
          ],
        },
        state: {
          name: "State",
          type: "list",
          options: [
            {
              AL: "Alabama",
            },
            {
              AK: "Alaska",
            },
            {
              AZ: "Arizona",
            },
            {
              AR: "Arkansas",
            },
            {
              CA: "California",
            },
            {
              CO: "Colorado",
            },
            {
              CT: "Connecticut",
            },
            {
              DE: "Delaware",
            },
            {
              DC: "District of Columbia",
            },
          ],
        },
        city: {
          name: "City",
          type: "list",
          options: [
            {
              "Fort Lauderdale": "Fort Lauderdale, FL USA",
            },
            {
              "River Forest": "River Forest, IL USA",
            },
            {
              "Poplar Grove": "Poplar Grove, IL USA",
            },
            {
              Claxton: "Claxton, GA USA",
            },
            {
              Fremont: "Fremont, MI USA",
            },
            {
              Philadelphia: "Philadelphia, PA USA",
            },
          ],
        },
        zip_code: {
          name: "Zip",
          type: "list",
          options: [
            {
              33332: "33332, Fort Lauderdale FL",
            },
            {
              60305: "60305, River Forest IL",
            },
            {
              61065: "61065, Poplar Grove IL",
            },
            {
              30417: "30417, Claxton GA",
            },
            {
              49412: "49412, Fremont MI",
            },
            {
              19129: "19129, Philadelphia PA",
            },
            {
              81506: "81506, Grand Junction CO",
            },
            {
              70445: "70445, Lacombe LA",
            },
            {
              70665: "70665, Sulphur LA",
            },
            {
              93646: "93646, Orange Cove CA",
            },
          ],
        },
      },
    },
  },
}
export default attributeRules
