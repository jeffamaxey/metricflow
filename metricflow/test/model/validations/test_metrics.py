import pytest

from metricflow.model.model_validator import ModelValidator
from metricflow.model.objects.data_source import DataSource, Mutability, MutabilityType
from metricflow.model.objects.elements.dimension import Dimension, DimensionType, DimensionTypeParams
from metricflow.model.objects.elements.identifier import Identifier, IdentifierType
from metricflow.model.objects.elements.measure import Measure, AggregationType
from metricflow.model.objects.metric import Metric, MetricType, MetricTypeParams
from metricflow.model.objects.user_configured_model import UserConfiguredModel
from metricflow.model.validations.validator_helpers import ModelValidationException
from metricflow.specs import TimeDimensionReference
from metricflow.time.time_granularity import TimeGranularity


@pytest.mark.skip("TODO: Will convert to validation rule")
def test_metric_missing_measure() -> None:  # noqa:D
    with pytest.raises(ModelValidationException):
        measure_name = "my_measure"
        measure2_name = "nonexistent_measure"
        ModelValidator.checked_validations(
            UserConfiguredModel(
                data_sources=[
                    DataSource(
                        name="sum_measure",
                        sql_query="SELECT foo FROM bar",
                        measures=[Measure(name=measure_name, agg=AggregationType.SUM)],
                        mutability=Mutability(type=MutabilityType.IMMUTABLE),
                    )
                ],
                metrics=[
                    Metric(
                        name="metric_with_nonexistent_measure",
                        type=MetricType.MEASURE_PROXY,
                        type_params=MetricTypeParams(measures=[measure2_name]),
                    )
                ],
            )
        )


def test_metric_no_time_dim_dim_only_source() -> None:  # noqa:D
    dim_name = "country"
    dim2_name = "ename"
    measure_name = "foo"
    ModelValidator.checked_validations(
        UserConfiguredModel(
            data_sources=[
                DataSource(
                    name="sum_measure",
                    sql_query="SELECT foo, country FROM bar",
                    measures=[],
                    dimensions=[Dimension(name=dim_name, type=DimensionType.CATEGORICAL)],
                    mutability=Mutability(type=MutabilityType.IMMUTABLE),
                ),
                DataSource(
                    name="sum_measure2",
                    sql_query="SELECT foo, country FROM bar",
                    measures=[
                        Measure(
                            name=measure_name,
                            agg=AggregationType.SUM,
                            agg_time_dimension=TimeDimensionReference(element_name=dim2_name),
                        )
                    ],
                    dimensions=[
                        Dimension(name=dim_name, type=DimensionType.CATEGORICAL),
                        Dimension(
                            name=dim2_name,
                            type=DimensionType.TIME,
                            type_params=DimensionTypeParams(
                                is_primary=True,
                                time_granularity=TimeGranularity.DAY,
                            ),
                        ),
                    ],
                    mutability=Mutability(type=MutabilityType.IMMUTABLE),
                ),
            ],
            metrics=[
                Metric(
                    name="metric_with_no_time_dim",
                    type=MetricType.MEASURE_PROXY,
                    type_params=MetricTypeParams(measures=[measure_name]),
                )
            ],
            materializations=[],
        )
    )


def test_metric_no_time_dim() -> None:  # noqa:D
    with pytest.raises(ModelValidationException):
        dim_name = "country"
        measure_name = "foo"
        ModelValidator.checked_validations(
            UserConfiguredModel(
                data_sources=[
                    DataSource(
                        name="sum_measure",
                        sql_query="SELECT foo, country FROM bar",
                        measures=[Measure(name=measure_name, agg=AggregationType.SUM)],
                        dimensions=[
                            Dimension(
                                name=dim_name,
                                type=DimensionType.CATEGORICAL,
                            )
                        ],
                        mutability=Mutability(type=MutabilityType.IMMUTABLE),
                    )
                ],
                metrics=[
                    Metric(
                        name="metric_with_no_time_dim",
                        type=MetricType.MEASURE_PROXY,
                        type_params=MetricTypeParams(measures=[measure_name]),
                    )
                ],
                materializations=[],
            )
        )


def test_metric_multiple_primary_time_dims() -> None:  # noqa:D
    with pytest.raises(ModelValidationException):
        dim_name = "date_created"
        dim2_name = "date_deleted"
        measure_name = "foo"
        ModelValidator.checked_validations(
            UserConfiguredModel(
                data_sources=[
                    DataSource(
                        name="sum_measure",
                        sql_query="SELECT foo, date_created, date_deleted FROM bar",
                        measures=[Measure(name=measure_name, agg=AggregationType.SUM)],
                        dimensions=[
                            Dimension(
                                name=dim_name,
                                type=DimensionType.TIME,
                                type_params=DimensionTypeParams(
                                    time_granularity=TimeGranularity.DAY,
                                ),
                            ),
                            Dimension(
                                name=dim2_name,
                                type=DimensionType.TIME,
                                type_params=DimensionTypeParams(
                                    time_granularity=TimeGranularity.DAY,
                                ),
                            ),
                        ],
                        mutability=Mutability(type=MutabilityType.IMMUTABLE),
                    )
                ],
                metrics=[
                    Metric(
                        name="foo",
                        type=MetricType.MEASURE_PROXY,
                        type_params=MetricTypeParams(measures=[measure_name]),
                    )
                ],
                materializations=[],
            )
        )


def test_generated_metrics_only() -> None:  # noqa:D
    dim_name = "dim"
    dim2_name = "ds"
    measure_name = "measure"
    identifier_name = "primary"
    data_source = DataSource(
        name="dim1",
        sql_query=f"SELECT {dim_name}, {measure_name} FROM bar",
        measures=[
            Measure(
                name=measure_name,
                agg=AggregationType.SUM,
                agg_time_dimension=TimeDimensionReference(element_name=dim2_name),
            )
        ],
        dimensions=[
            Dimension(name=dim_name, type=DimensionType.CATEGORICAL),
            Dimension(
                name=dim2_name,
                type=DimensionType.TIME,
                type_params=DimensionTypeParams(
                    is_primary=True,
                    time_granularity=TimeGranularity.DAY,
                ),
            ),
        ],
        mutability=Mutability(type=MutabilityType.IMMUTABLE),
        identifiers=[
            Identifier(name=identifier_name, type=IdentifierType.PRIMARY),
        ],
    )
    data_source.measures[0].create_metric = True

    ModelValidator.checked_validations(
        UserConfiguredModel(
            data_sources=[data_source],
            metrics=[],
            materializations=[],
        )
    )
