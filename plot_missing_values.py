#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import matplotlib.pyplot as plt 


def nullity_sort(df, sort=None, axis='columns'):
    """
    Sorts a DataFrame according to its nullity, in either ascending or descending order.
    :param df: The DataFrame object being sorted.
    :param sort: The sorting method: either "ascending", "descending", or None (default).
    :return: The nullity-sorted DataFrame.
    """
    if sort is None:
        return df
    elif sort not in ['ascending', 'descending']:
        raise ValueError('The "sort" parameter must be set to "ascending" or "descending".')

    if axis not in ['rows', 'columns']:
        raise ValueError('The "axis" parameter must be set to "rows" or "columns".')

    if axis == 'columns':
        if sort == 'ascending':
            return df.iloc[np.argsort(df.count(axis='columns').values), :]
        elif sort == 'descending':
            return df.iloc[np.flipud(np.argsort(df.count(axis='columns').values)), :]
    elif axis == 'rows':
        if sort == 'ascending':
            return df.iloc[:, np.argsort(df.count(axis='rows').values)]
        elif sort == 'descending':
            return df.iloc[:, np.flipud(np.argsort(df.count(axis='rows').values))]


def nullity_filter(df, filter=None, p=0, n=0):
    """
    Filters a DataFrame according to its nullity, using some combination of 'top' and 'bottom' numerical and
    percentage values. Percentages and numerical thresholds can be specified simultaneously: for example,
    to get a DataFrame with columns of at least 75% completeness but with no more than 5 columns, use
    `nullity_filter(df, filter='top', p=.75, n=5)`.
    :param df: The DataFrame whose columns are being filtered.
    :param filter: The orientation of the filter being applied to the DataFrame. One of, "top", "bottom",
    or None (default). The filter will simply return the DataFrame if you leave the filter argument unspecified or
    as None.
    :param p: A completeness ratio cut-off. If non-zero the filter will limit the DataFrame to columns with at least p
    completeness. Input should be in the range [0, 1].
    :param n: A numerical cut-off. If non-zero no more than this number of columns will be returned.
    :return: The nullity-filtered `DataFrame`.
    """
    if filter == 'top':
        if p:
            df = df.iloc[:, [c >= p for c in df.count(axis='rows').values / len(df)]]
        if n:
            df = df.iloc[:, np.sort(np.argsort(df.count(axis='rows').values)[-n:])]
    elif filter == 'bottom':
        if p:
            df = df.iloc[:, [c <= p for c in df.count(axis='rows').values / len(df)]]
        if n:
            df = df.iloc[:, np.sort(np.argsort(df.count(axis='rows').values)[:n])]
    return df

def missing_values_bars(
    df, figsize=None, fontsize=16, labels=None, label_rotation=45, log=False, color='dimgray',
    filter=None, n=0, p=0, sort=None, ax=None, orientation=None
):

    df = nullity_filter(df, filter=filter, n=n, p=p)
    df = nullity_sort(df, sort=sort, axis='rows')
    nullity_counts = len(df) - df.isin(['-1', -1, np.nan]).sum()


    if orientation is None:
        if len(df.columns) > 50:
            orientation = 'left'
        else:
            orientation = 'bottom'

    if ax is None:
        ax1 = plt.gca()
        if figsize is None:
            if len(df.columns) <= 50 or orientation == 'top' or orientation == 'bottom':
                figsize = (25, 10)
            else:
                figsize = (25, (25 + len(df.columns) - 50) * 0.5)
    else:
        ax1 = ax
        figsize = None  # for behavioral consistency with other plot types, re-use the given size

    plot_args = {'figsize': figsize, 'fontsize': fontsize, 'log': log, 'color': color, 'ax': ax1}
    if orientation == 'bottom':
        (nullity_counts / len(df)).plot.bar(**plot_args)
    else:
        (nullity_counts / len(df)).plot.barh(**plot_args)

    axes = [ax1]

    # Start appending elements, starting with a modified bottom x axis.
    if labels or (labels is None and len(df.columns) <= 50):
        ax1.set_xticklabels(
            ax1.get_xticklabels(), rotation=label_rotation, ha='right', fontsize=fontsize
        )

        # Create the numerical ticks.
        ax2 = ax1.twinx()
        axes.append(ax2)
        if not log:
            ax1.set_ylim([0, 1])
            ax2.set_yticks(ax1.get_yticks())
            ax2.set_yticklabels([int(n * len(df)) for n in ax1.get_yticks()], fontsize=fontsize)
        else:
            # For some reason when a logarithmic plot is specified `ax1` always contains two more ticks than actually
            # appears in the plot. The fix is to ignore the first and last entries. Also note that when a log scale
            # is used, we have to make it match the `ax1` layout ourselves.
            ax2.set_yscale('log')
            ax2.set_ylim(ax1.get_ylim())
        ax2.set_yticklabels([int(n * len(df)) for n in ax1.get_yticks()], fontsize=fontsize)

        # Create the third axis, which displays columnar totals above the rest of the plot.
        ax3 = ax1.twiny()
        axes.append(ax3)
        ax3.set_xticks(ax1.get_xticks())
        ax3.set_xlim(ax1.get_xlim())
        ax3.set_xticklabels(
            nullity_counts.values, fontsize=fontsize, rotation=label_rotation, ha='left'
        )
    else:
        # Create the numerical ticks.
        ax2 = ax1.twinx()

        axes.append(ax2)
        if not log:
            # Width
            ax1.set_xlim([0, 1])

            # Bottom
            ax2.set_xticks(ax1.get_xticks())
            ax2.set_xticklabels([int(n * len(df)) for n in ax1.get_xticks()], fontsize=fontsize)

            # Right
            ax2.set_yticks(ax1.get_yticks())
            ax2.set_yticklabels(nullity_counts.values, fontsize=fontsize, ha='left')
        else:
            # For some reason when a logarithmic plot is specified `ax1` always contains two more ticks than actually
            # appears in the plot. The fix is to ignore the first and last entries. Also note that when a log scale
            # is used, we have to make it match the `ax1` layout ourselves.
            ax1.set_xscale('log')
            ax1.set_xlim(ax1.get_xlim())

            # Bottom
            ax2.set_xticks(ax1.get_xticks())
            ax2.set_xticklabels([int(n * len(df)) for n in ax1.get_xticks()], fontsize=fontsize)

            # Right
            ax2.set_yticks(ax1.get_yticks())
            ax2.set_yticklabels(nullity_counts.values, fontsize=fontsize, ha='left')

        # Create the third axis, which displays columnar totals above the rest of the plot.
        ax3 = ax1.twiny()

        axes.append(ax3)
        ax3.set_yticks(ax1.get_yticks())
        if log:
            ax3.set_xscale('log')
            ax3.set_xlim(ax1.get_xlim())
        ax3.set_ylim(ax1.get_ylim())

    ax3.grid(False)

    for ax in axes:
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.xaxis.set_ticks_position('none')
        ax.yaxis.set_ticks_position('none')

    return ax1

