
request1 = {
    "reportScope": {
        "agencyId": 20700000000002001
    },
    "reportType": "adGroup",
    "columns": [
        {
            "columnName": "date",
            "headerText": "Date"
        },
        {
            "columnName": "advertiser",
            "headerText": "Annonceur"
        },
        {
            "columnName": "account",
            "headerText": "Account"
        },
        {
            "columnName": "accountType",
            "headerText": "Publisher"
        },
        {
            "columnName": "campaign",
            "headerText": "Campaign"
        },
        {
            "columnName": "adgroup",
            "headerText": "Adgroup"
        },
        {
            "columnName": "status",
            "headerText": "Status"
        },
        {
            "columnName": "deviceSegment",
            "headerText": "Device"
        },
        {
            "columnName": "floodlightGroup",
            "headerText": "FloodlightType"
        },
        {
            "columnName": "dfaActions",
            "headerText": "DFAActions"
        },
        {
            "columnName": "dfaTransactions",
            "headerText": "DFATransactions"
        },
        {
            "columnName": "dfaWeightedActions",
            "headerText": "DFAWeightedActions"
        }
    ],
          "timeRange": {
              "startDate": "",
              "endDate": ""
          },
          "filters": [
              {
                  "column": {
                      "columnName": "advertiser",
                      "headerText": "Annonceur"
                  },
                  "operator": "startsWith",
                  "values": [
                      "ELCE"
                  ]
              }
          ],
          "includeDeletedEntities": "false",
          "statisticsCurrency": "agency",
          "downloadFormat": "csv",
          "maxRowsPerFile": 1000000
          }


schema1 = {
          'fields': [
            {'name': 'Date', 'type': 'STRING'},
            {'name': 'Annonceur', 'type': 'STRING'},
            {'name': 'Account', 'type': 'STRING'},
            {'name': 'Publisher', 'type': 'STRING'},
            {'name': 'Campaign', 'type': 'STRING'},
            {'name': 'Adgroup', 'type': 'STRING'},
            {'name': 'Status', 'type': 'STRING'},
            {'name': 'Device', 'type': 'STRING'},
            {'name': 'FloodlightActivity', 'type': 'STRING'},
            {'name': 'DFAActions', 'type': 'INTEGER'},
            {'name': 'DFATransactions', 'type': 'INTEGER'},
            {'name': 'DFAWeightedActions', 'type': 'FLOAT'}
        ]
          }



request2 = {
          "reportScope": {
              "agencyId": "20700000000002001"
          },
          "reportType": "adGroup",
          "columns": [
              {
                "columnName": "date",
                "headerText": "Date",
              },
              {
                "columnName": "advertiser",
                "headerText": "Annonceur",
              },
              {
                "columnName": "account",
                "headerText": "Account",
              },
              {
                "columnName": "accountType",
                "headerText": "Publisher",
              },
              {
                "columnName": "campaign",
                "headerText": "Campaign",
              },
              {
                "columnName": "adgroup",
                "headerText": "Adgroup",
              },
              {
                "columnName": "status",
                "headerText": "Status",
              },
              {
                "columnName": "adGroupLabels",
                "headerText": "Labels",
              },
              {
                "columnName": "effectiveLabels",
                "headerText": "LabelsHerite",
              },
              {
                "columnName": "deviceSegment",
                "headerText": "Device",
              },
              {
                "columnName": "countryTargets",
                "headerText": "CiblageGeoPays",
              },
              {
                "columnName": "effectiveCountryTargets",
                "headerText": "CiblageGeoPaysHerite",
              },
              {
                "columnName": "cityTargets",
                "headerText": "CiblageGeoCity",
              },
              {
                "columnName": "effectiveCityTargets",
                "headerText": "CiblageGeoCityHerite",
              },
              {
                "columnName": "adGroupMobileBidAdjustment",
                "headerText": "AdGroupMobileBidAdjustment",
              },
              {
                "columnName": "adGroupLabels",
                "headerText": "AdGroupLabels",
              },
              {
                "columnName": "effectiveLabels",
                "headerText": "AdGroupLabelsHerite",
              },
              {
                "columnName": "impr",
                "headerText": "Impression",
              },
              {
                "columnName": "clicks",
                "headerText": "Clicks",
              },
              {
                "columnName": "avgPos",
                "headerText": "Position",
              },
              {
                "columnName": "cost",
                "headerText": "Cost",
              },
              {
                "columnName": "dfaRevenue",
                "headerText": "Revenu",
              },
              {
                "columnName": "visits",
                "headerText": "Visite",
              },
              {
                "columnName": "adWordsConversions",
                "headerText": "AdWordsConversions",
              },
              {
                "columnName": "searchImpressionShare",
                "headerText": "ImpShare",
              },
              {
                "columnName": "searchRankLostImpressionShare",
                "headerText": "LostISRank",
              }
          ],
          "timeRange": {
              "startDate": "",
              "endDate": ""
          },
          "filters": [
              {
                  "column": {
                      "columnName": "advertiser",
                      "headerText": "Annonceur"
                  },
                  "operator": "startsWith",
                  "values": [
                      "ELCE"
                  ]
              }
          ],
          "includeDeletedEntities": "false",
          "statisticsCurrency": "agency",
          "downloadFormat": "csv",
          "maxRowsPerFile": 1000000
          }


schema2 = {
          'fields': [
            {'name': 'Date', 'type': 'STRING'},
            {'name': 'Annonceur', 'type': 'STRING'},
            {'name': 'Account', 'type': 'STRING'},
            {'name': 'Publisher', 'type': 'STRING'},
            {'name': 'Campaign', 'type': 'STRING'},
            {'name': 'Adgroup', 'type': 'STRING'},
            {'name': 'Status', 'type': 'STRING'},
            {'name': 'Labels', 'type': 'STRING'},
            {'name': 'LabelsHerite', 'type': 'STRING'},
            {'name': 'Device', 'type': 'STRING'},
            {'name': 'CiblageGeoPays', 'type': 'STRING'},
            {'name': 'CiblageGeoPaysHerite', 'type': 'STRING'},
            {'name': 'CiblageGeoCity', 'type': 'STRING'},
            {'name': 'CiblageGeoCityHerite', 'type': 'STRING'},
            {'name': 'AdGroupMobileBidAdjustment', 'type': 'FLOAT'}, #
            {'name': 'AdGroupLabels', 'type': 'STRING'},
            {'name': 'AdGroupLabelsHerite', 'type': 'STRING'}, 
            {'name': 'Impression', 'type': 'INTEGER'},
            {'name': 'Clicks', 'type': 'INTEGER'},
            {'name': 'Position', 'type': 'FLOAT'},
            {'name': 'Cost', 'type': 'FLOAT'}, #
            {'name': 'Revenu', 'type': 'FLOAT'},
            {'name': 'Visite', 'type': 'INTEGER'},
            {'name': 'AdWordsConversions', 'type': 'INTEGER'},
            {'name': 'ImpShare', 'type': 'STRING'}, #
            {'name': 'LostISRank', 'type': 'STRING'} #
                    ]
          }


left_join_qry =  """ SELECT t2.Date AS Date,
                            t2.Annonceur AS Annonceur,
                            t2.Account AS Account,
                            t2.Publisher AS Publisher,
                            t2.Campaign AS Campaign,
                            t2.Adgroup AS Adgroup,
                            t2.Status AS Status,
                            t2.Labels AS Labels,
                            t2.LabelsHerite AS LabelsHerite,
                            t2.Device AS Device,
                            t2.CiblageGeoPays AS CiblageGeoPays,
                            t2.CiblageGeoPaysHerite AS CiblageGeoPaysHerite,
                            t2.CiblageGeoCity AS CiblageGeoCity,
                            t2.CiblageGeoCityHerite AS CiblageGeoCityHerite,
                            t2.AdGroupMobileBidAdjustment AS AdGroupMobileBidAdjustment,
                            t2.AdGroupLabels AS AdGroupLabels,
                            t2.AdGroupLabelsHerite AS AdGroupLabelsHerite,
                            t2.Impression AS Impression,
                            t2.Clicks AS Clicks,
                            t2.Position AS Position,
                            t2.Cost AS Cost,
                            t2.Revenu AS Revenu,
                            t2.Visite AS Visite,
                            t2.AdWordsConversions AS AdWordsConversions,
                            t2.ImpShare AS ImpShare,
                            t2.LostISRank AS LostISRank,
                            t1.FloodlightActivity AS FloodlightActivity,
                            t1.DFAActions AS DFAActions,
                            t1.DFATransactions AS DFATransactions,
                            t1.DFAWeightedActions AS DFAWeightedActions,
                            t2.Impression * t2.Position AS Posimp FROM 
                     (SELECT *, IFNULL(Device, "null") AS Device_ FROM elce_ds_reports.ds_report_2_%s) AS t2
                 LEFT JOIN
                     (SELECT *, IFNULL(Device, "null") AS Device_ FROM elce_ds_reports.ds_report_1_%s WHERE UPPER(FloodlightActivity) CONTAINS "CONV" OR UPPER(FloodlightActivity) CONTAINS "OPTIN") AS t1
                               ON t1.Annonceur = t2.Annonceur
                               AND t1.Account = t2.Account
                               AND t1.Publisher = t2.Publisher
                               AND t1.Campaign = t2.Campaign
                               AND t1.Adgroup = t2.Adgroup
                               AND t1.Device_ = t2.Device_ """
