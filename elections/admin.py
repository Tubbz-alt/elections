# -*- coding: utf-8 -*-
#
# Copyright © 2008 Nigel Jones, Toshio Kuratomi, Ricky Zhou, Luca Foppiano All rights reserved.
#
# This copyrighted material is made available to anyone wishing to use, modify,
# copy, or redistribute it subject to the terms and conditions of the GNU
# General Public License v.2.  This program is distributed in the hope that it
# will be useful, but WITHOUT ANY WARRANTY expressed or implied, including the
# implied warranties of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.  You should have
# received a copy of the GNU General Public License along with this program;
# if not, write to the Free Software Foundation, Inc., 51 Franklin Street,
# Fifth Floor, Boston, MA 02110-1301, USA. Any Red Hat trademarks that are
# incorporated in the source code or documentation are not subject to the GNU
# General Public License and may only be used or replicated with the express
# permission of Red Hat, Inc.
#
# Author(s): Nigel Jones <nigelj@fedoraproject.org>
#            Toshio Kuratomi <toshio@fedoraproject.org>
#            Ricky Zhou <ricky@fedoraproject.org>
#            Luca Foppiano <lfoppiano@fedoraproject.org>
#
# Report Bugs to https://www.fedorahosted.org/elections


# Admin functions go here (i.e. add/delete elections)

import turbogears
from turbogears import controllers, expose, flash, redirect, config
from turbogears import identity
from elections import model
from elections.model import Elections, ElectionsTable, Candidates, LegalVoters

from datetime import datetime

import sqlalchemy

from turbogears.database import session

class Admin(controllers.Controller):
    def __init__(self, fas, appTitle):
        self.fas = fas
        self.appTitle = appTitle

    @expose(allow_json=True)
    def list_elections(self, **kw):
        electlist = Elections.query.order_by(ElectionsTable.c.start_date).filter('id>0').all()
        elections = [{'id': e.id, 'alias': e.alias, 'shortdesc': e.shortdesc, 'start_date': e.start_date, 'end_date': e.end_date, 'legal_voters': [{'groupname': lv.group_name} for lv in LegalVoters.query.filter_by(election_id=e.id)]} for e in electlist]
        return dict(elections=elections, servertime=datetime.utcnow(), appTitle=self.appTitle)

    @expose(template='elections.templates.admin')
    @identity.require(identity.in_group("elections"))
    def index(self, **kw):
        electlist = Elections.query.order_by(ElectionsTable.c.start_date).filter('id>0').all()
        elections = [{'id': e.id, 'alias': e.alias, 'shortdesc': e.shortdesc, 'start_date': e.start_date, 'end_date': e.end_date, 'legal_voters': [{'groupname': lv.group_name} for lv in LegalVoters.query.filter_by(election_id=e.id)], 'embargoed' : e.embargoed} for e in electlist]
        return dict(elections=elections)
    
    @identity.require(identity.in_group("elections"))
    @expose(template="elections.templates.admnewe")
    def newe(self, **kw):        
        if "submit" in kw:
            setembargo=1
            usefas=1
            if "embargoed" not in kw:
                setembargo=0
            if "usefas" not in kw:
                usefas=0

            Elections(alias=kw['alias'], status=0, method=0, shortdesc=kw['shortdesc'], description=kw['info'], url=kw['url'], start_date=kw['startdate'], end_date=kw['enddate'], embargoed=setembargo, seats_elected=kw['seats'],usefas=usefas,votes_per_user=1)
            raise turbogears.redirect("/")
        else:
            return dict()

    @identity.require(identity.in_group("elections"))
    @expose(template="elections.templates.admnewc")
    def newc(self, **kw):        
        if "submit" in kw:
            for entry in kw['nameurl'].split("|"):
                candidate = entry.split("!")
                #Python doesn't have a good way of doing case/switch statements
                if len(candidate) == 1:
                    Candidates(election_id=kw['id'],name=candidate[0], status=0, human=1)
                elif len(candidate) == 2:
                    Candidates(election_id=kw['id'],name=candidate[0],url=candidate[1], status=0, human=1)
                else:
                    turbogears.flash("There was an issue!")
            raise turbogears.redirect("/admin/newc")
        else:
            return dict()

    @identity.require(identity.in_group("elections"))
    @expose(template="elections.templates.admedit")
    def edit(self,eid=None):
        try:
            election = Elections.query.filter_by(id=int(eid)).all()[0]
        except ValueError:
            election = Elections.query.filter_by(alias=eid).all()[0]
        candidates = Candidates.query.filter_by(election_id=election.id).all()
	votergroups = LegalVoters.query.filter_by(election_id=election.id).all()
        return dict(e=election, candidates=candidates, groups=votergroups)
