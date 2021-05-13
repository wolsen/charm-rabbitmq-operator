#!/usr/bin/env python3

"""
Work in progress interface for AMQP relations
"""

import logging

from ops.framework import (
    StoredState,
    EventBase,
    ObjectEvents,
    EventSource,
    Object)


class HasPeersEvent(EventBase):
    """Has Peers Event."""
    pass


class ReadyPeersEvent(EventBase):
    pass


class RabbitMQOperatorPeerEvents(ObjectEvents):
    has_peers = EventSource(HasPeersEvent)
    ready_peers = EventSource(ReadyPeersEvent)


class RabbitMQOperatorPeers(Object):

    on = RabbitMQOperatorPeerEvents()
    state = StoredState()
    OPERATOR_PASSWORD = "operator_password"
    OPERATOR_USER_CREATED = "operator_user_created"

    def __init__(self, charm, relation_name):
        super().__init__(charm, relation_name)
        self.relation_name = relation_name
        self.framework.observe(
            charm.on[relation_name].relation_joined,
            self.on_joined)
        self.framework.observe(
            charm.on[relation_name].relation_changed,
            self.on_changed)

    @property
    def peers_rel(self):
        return self.framework.model.get_relation(self.relation_name)

    def on_joined(self, event):
        logging.info("RabbitMQOperatorPeers on_joined")
        self.on.has_peers.emit()

    def on_changed(self, event):
        logging.info("RabbitMQOperatorPeers on_changed")
        # TODO check for some data on the relation
        self.on.ready_peers.emit()

    def set_operator_password(self, password):
        logging.info("Setting operator password")
        self.peers_rel.data[self.peers_rel.app][self.OPERATOR_PASSWORD] = password

    def set_operator_user_created(self, user):
        logging.info("Setting operator user created")
        self.peers_rel.data[self.peers_rel.app][self.OPERATOR_USER_CREATED] = user

    @property
    def operator_password(self):
        if not self.peers_rel:
            return None
        return self.peers_rel.data[self.peers_rel.app].get(self.OPERATOR_PASSWORD)

    @property
    def operator_user_created(self):
        if not self.peers_rel:
            return None
        return self.peers_rel.data[
            self.peers_rel.app].get(self.OPERATOR_USER_CREATED)