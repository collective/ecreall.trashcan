domain=ecreall.trashcan
i18ndude rebuild-pot --pot locales/$domain.pot --create $domain .
i18ndude sync --pot locales/$domain.pot locales/*/LC_MESSAGES/$domain.po

i18ndude rebuild-pot --pot locales/plone.pot --create plone .
i18ndude sync --pot locales/plone.pot locales/*/LC_MESSAGES/plone.po
